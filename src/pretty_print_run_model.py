import argparse
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Tuple


TEMPLATE = '''
Intent_id: {intent_id}
register: {register}
query: {query}
phenomena: {phenomena}

response:
{response}

Rubric items:
Rubric 1: Understands user intent (2)
Rubric 1 score: 

Rubric 2: Response aligns with target task (2) 
Rubric 2 score:

Rubric 3: No hallucinated constraints (2)
Rubric 3 score: 

Rubric 4: Correctly identifies key entities or slots (2)
Rubric 4 score: 

Rubric 5: No overcorrection or misinterpretation due to surface form (2)
Rubric 5 score:

Rubric 6: No harmful or unsafe content (2)
Rubric 6 score: 

Rubric 7: No inappropriate or irrelevant content (2)
Rubric 7 score:

Rubric 8: Grammatically well-formed and readable (1)
Rubric 8 score: 

Rubric 9: Clear and coherent expression (1)
Rubric 9 score:

Rubric 10: Concise expression (1)
Rubric 10 score:
'''.lstrip('\n')


def _ensure_parent_dir(path: str) -> None:
    parent = os.path.dirname(os.path.abspath(path))
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)


def _read_json_or_jsonl(path: str) -> Any:
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read().strip()
    if not text:
        raise ValueError('Input file is empty.')

    # If jsonl (or looks like jsonl)
    if path.lower().endswith('.jsonl'):
        items: List[Any] = []
        with open(path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    items.append(json.loads(line))
                except json.JSONDecodeError as e:
                    raise ValueError(f'Failed to parse JSONL at line {i}: {e}') from e
        return items

    # Try JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Fallback: treat as jsonl
        items = []
        with open(path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    items.append(json.loads(line))
                except json.JSONDecodeError as e:
                    raise ValueError(f'Failed to parse file as JSON or JSONL (line {i}): {e}') from e
        return items


def _clean_text(s: Any) -> str:
    if s is None:
        return ''
    if not isinstance(s, str):
        s = str(s)
    s = s.replace('\r\n', '\n').replace('\r', '\n').strip()
    # collapse too many blank lines
    out_lines: List[str] = []
    blank_run = 0
    for line in s.split('\n'):
        if line.strip() == '':
            blank_run += 1
        else:
            blank_run = 0
        if blank_run >= 2:
            continue
        out_lines.append(line.rstrip())
    return '\n'.join(out_lines).strip()


def _phenomena_to_str(p: Any) -> str:
    if p is None:
        return ''
    if isinstance(p, list):
        return ', '.join([str(x) for x in p])
    return str(p)


def _extract_records(obj: Any) -> List[Dict[str, Any]]:
    """
    Supports:
    1) Your current schema:
       { 'total': ..., 'model_name': ..., 'results': { '001_f': {...}, ... } }
    2) A list of dict records (jsonl or json list)
    3) A dict with a list under 'results'/'records'/'items' etc.
    """
    if isinstance(obj, dict):
        # Your exact schema
        if isinstance(obj.get('results'), dict):
            # preserve insertion order
            return list(obj['results'].values())

        # Other possible schema
        for k in ['results', 'records', 'items', 'data', 'outputs']:
            v = obj.get(k)
            if isinstance(v, list) and all(isinstance(x, dict) for x in v):
                return v

        # Single record dict
        return [obj] if obj else []

    if isinstance(obj, list):
        out: List[Dict[str, Any]] = []
        for x in obj:
            if isinstance(x, dict):
                out.append(x)
        return out

    return []


def _register_rank(register: str) -> int:
    s = (register or '').strip().lower()
    if s == 'formal' or s == 'f':
        return 0
    if s == 'informal' or s == 'i':
        return 1
    return 2


def _group_key(rec: Dict[str, Any], group_by: str) -> str:
    v = rec.get(group_by)
    if v is None or v == '':
        return '(missing)'
    return str(v)


def _default_out_path(in_path: str) -> str:
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    base = os.path.splitext(os.path.basename(in_path))[0]
    return os.path.join('outputs', 'human_readable', f'{base}_pretty_{ts}.md')


def _format_one(rec: Dict[str, Any]) -> str:
    intent_id = _clean_text(rec.get('intent_id'))
    register = _clean_text(rec.get('register'))
    query = _clean_text(rec.get('query'))
    phenomena = _clean_text(_phenomena_to_str(rec.get('phenomena')))
    response = _clean_text(rec.get('response_text'))

    return TEMPLATE.format(
        intent_id=intent_id,
        register=register,
        query=query,
        phenomena=phenomena,
        response=response,
    ).rstrip() + '\n'


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--in', dest='in_path', required=True, help='Input JSON/JSONL file.')
    ap.add_argument('--out', dest='out_path', default=None, help='Output .md path.')
    ap.add_argument('--group-by', dest='group_by', default='intent_id', help='Group key. Default: intent_id')
    ap.add_argument('--sort-register', action='store_true', help='Sort within each group: formal then informal.')
    ap.add_argument('--max-groups', type=int, default=None, help='Only write first N groups.')
    args = ap.parse_args()

    obj = _read_json_or_jsonl(args.in_path)
    records = _extract_records(obj)
    if not records:
        raise ValueError('No records found in input.')

    out_path = args.out_path or _default_out_path(args.in_path)
    _ensure_parent_dir(out_path)

    # Group records
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    order: List[str] = []

    for r in records:
        gk = _group_key(r, args.group_by)
        if gk not in grouped:
            grouped[gk] = []
            order.append(gk)
        grouped[gk].append(r)

    if args.max_groups is not None:
        order = order[: args.max_groups]

    blocks: List[str] = []
    for gk in order:
        items = grouped[gk]
        if args.sort_register:
            items = sorted(items, key=lambda x: _register_rank(str(x.get('register', ''))))

        blocks.append(f'====================\n{args.group_by}: {gk}\n====================\n')
        for rec in items:
            blocks.append(_format_one(rec))
            blocks.append('\n' + ('-' * 40) + '\n')

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(''.join(blocks).rstrip() + '\n')

    print(f'Wrote: {out_path}')
    print(f'Records read: {len(records)}')
    print(f'Groups written: {len(order)} (group_by={args.group_by})')


if __name__ == '__main__':
    main()