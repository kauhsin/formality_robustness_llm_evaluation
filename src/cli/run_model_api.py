import sys
import json


def call_model_api(prompt: str) -> str:
    """
    Temporary stub for Day 12: returns a constant string so the pipeline can run.
    Replace with a real API call on Day 13.
    """
    return 'STUB_RESPONSE'


def main(input_path: str, output_path: str) -> None:
    total = 0
    results = {}

    valid_phenomena = {'abbreviation', 'dialect_word', 'informal_lexicon', 'noncanonical_syntax', 'typo'}

    # Placeholders to be replaced/updated on Day 13
    model_name = 'api_model_tbd'
    notes = 'api runner placeholder; call_model_api not implemented yet'

    with open(input_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()

            # Skip empty lines and comment lines
            if not line or line.startswith('#'):
                continue

            try:
                obj = json.loads(line)

                sample_id = obj.get('id', 'unknown').lower().strip()
                if sample_id == 'unknown':
                    continue

                intent_id = obj.get('intent_id', 'unknown').lower().strip()
                if intent_id == 'unknown':
                    continue

                register = obj.get('register', 'unknown').lower().strip()
                if register not in {'formal', 'informal'}:
                    continue

                phenomena_list = []
                raw_phenomena = obj.get('phenomena', [])
                for p in raw_phenomena:
                    clean_p = str(p).lower().strip()
                    if clean_p in valid_phenomena:
                        phenomena_list.append(clean_p)

                query = obj.get('query', 'unknown').strip()

                # Minimal prompt construction: use query directly
                prompt = query

                # On Day 13, this will produce real model output
                response_text = call_model_api(prompt)

                total += 1
                results[sample_id] = {
                    'id': sample_id,
                    'intent_id': intent_id,
                    'register': register,
                    'phenomena': phenomena_list,
                    'query': query,
                    'response_text': response_text,
                    'notes': notes
                }

            except json.JSONDecodeError:
                print(f'Row {line_num} is skipped due to JSONDecodeError')

    summary = {
        'total': total,
        'model_name': model_name,
        'results': results
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] in ('-h', '--help'):
        print('Usage: python3 src/cli/run_model_api.py <input_jsonl> --out <output_path>')
        sys.exit(0)

    if len(sys.argv) != 4 or sys.argv[2] != '--out':
        print('Usage: python3 src/cli/run_model_api.py <input_jsonl> --out <output_path>')
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[3]
    main(input_path, output_path)