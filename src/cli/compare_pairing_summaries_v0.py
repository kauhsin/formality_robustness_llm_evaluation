import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple


def _read_json(path: Path) -> Dict[str, Any]:
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def _safe_float(x: Any) -> float:
    try:
        return float(x)
    except Exception:
        return float('nan')


def _summarize_pairing(path: Path) -> Tuple[Dict[str, Any], List[str]]:
    errors: List[str] = []
    obj = _read_json(path)

    pairs = obj.get('pairs')
    if not isinstance(pairs, dict):
        return {}, [f'{path.name}: missing or invalid "pairs" (expected dict)']

    deltas: List[float] = []
    missing_delta_keys = 0
    malformed_pairs = 0

    for intent_id, entry in pairs.items():
        if not isinstance(entry, dict):
            malformed_pairs += 1
            continue

        if 'delta_informal_to_formal' not in entry:
            missing_delta_keys += 1
            continue

        d = _safe_float(entry.get('delta_informal_to_formal'))
        if d != d:  # NaN check
            malformed_pairs += 1
            continue

        deltas.append(d)

    total_pairs = len(pairs)
    used_pairs = len(deltas)

    if missing_delta_keys > 0:
        errors.append(f'{path.name}: {missing_delta_keys} pair(s) missing delta_informal_to_formal')
    if malformed_pairs > 0:
        errors.append(f'{path.name}: {malformed_pairs} malformed pair(s) (non-dict or non-numeric delta)')
    if used_pairs == 0:
        errors.append(f'{path.name}: no usable deltas found')

    avg_delta = sum(deltas) / used_pairs if used_pairs > 0 else 0.0
    num_informal_better = sum(1 for d in deltas if d > 0)
    num_formal_better = sum(1 for d in deltas if d < 0)
    num_ties = sum(1 for d in deltas if d == 0)

    # slice name: strip prefix/suffix
    name = path.name
    if name.startswith('pairing_'):
        name = name[len('pairing_'):]
    if name.endswith('.json'):
        name = name[:-len('.json')]

    summary = {
        'slice': name,
        'file': str(path),
        'total_pairs_reported': int(obj.get('total_pair_num')) if str(obj.get('total_pair_num', '')).isdigit() else total_pairs,
        'pairs_in_file': total_pairs,
        'pairs_used_for_stats': used_pairs,
        'avg_delta_informal_to_formal': avg_delta,
        'num_informal_better': num_informal_better,
        'num_formal_better': num_formal_better,
        'num_ties': num_ties
    }

    return summary, errors


def _print_table(rows: List[Dict[str, Any]]) -> None:
    # fixed columns
    headers = [
        'slice',
        'pairs',
        'used',
        'avg_delta',
        'inf_better',
        'formal_better',
        'ties'
    ]

    def fmt(row: Dict[str, Any]) -> List[str]:
        return [
            str(row.get('slice', '')),
            str(row.get('pairs_in_file', '')),
            str(row.get('pairs_used_for_stats', '')),
            f'{row.get("avg_delta_informal_to_formal", 0.0):.2f}',
            str(row.get('num_informal_better', '')),
            str(row.get('num_formal_better', '')),
            str(row.get('num_ties', ''))
        ]

    table = [headers] + [fmt(r) for r in rows]
    col_widths = [max(len(str(cell)) for cell in col) for col in zip(*table)]

    def join_line(cells: List[str]) -> str:
        return '  '.join(str(c).ljust(w) for c, w in zip(cells, col_widths))

    print(join_line(headers))
    print(join_line(['-' * w for w in col_widths]))
    for r in rows:
        print(join_line(fmt(r)))


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Compare pairing summary JSONs (pairing_*_pilot_v0.json) and print a small table.'
    )
    parser.add_argument(
        '--in_dir',
        default='outputs/after_api',
        help='Directory containing pairing summary JSONs'
    )
    parser.add_argument(
        '--pattern',
        default='pairing_*_pilot_v0.json',
        help='Glob pattern used to find pairing JSONs'
    )
    parser.add_argument(
        '--out_json',
        default='',
        help='Optional path to write combined JSON summary (leave empty to skip)'
    )

    args = parser.parse_args()
    in_dir = Path(args.in_dir)
    pattern = args.pattern

    if not in_dir.exists():
        raise FileNotFoundError(f'Input dir not found: {in_dir}')

    paths = sorted(in_dir.glob(pattern))
    if not paths:
        raise FileNotFoundError(f'No files matched pattern "{pattern}" in {in_dir}')

    all_rows: List[Dict[str, Any]] = []
    all_errors: List[str] = []

    for p in paths:
        row, errs = _summarize_pairing(p)
        if row:
            all_rows.append(row)
        all_errors.extend(errs)

    # sort by avg_delta ascending (more negative => informal worse)
    all_rows.sort(key=lambda r: r.get('avg_delta_informal_to_formal', 0.0))

    _print_table(all_rows)

    if all_errors:
        print('\nQA warnings:')
        for e in all_errors:
            print(f'- {e}')

    if args.out_json:
        out_path = Path(args.out_json)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_obj = {
            'meta': {
                'in_dir': str(in_dir),
                'pattern': pattern,
                'num_files': len(paths),
                'num_summaries': len(all_rows),
                'num_warnings': len(all_errors)
            },
            'summaries': all_rows,
            'warnings': all_errors
        }
        with out_path.open('w', encoding='utf-8') as f:
            json.dump(out_obj, f, indent=2)
        print(f'\nWrote combined summary JSON to: {out_path}')


if __name__ == '__main__':
    main()