import sys, json
from collections import Counter, defaultdict

def main(input_path, output_path):
    total = 0
    results = {}
    valid_phenomena = {'abbreviation', 'dialect_word', 'informal_lexicon', 'noncanonical_syntax', 'typo'}
# define the place holders
    model_name = 'stub_model'
    response_text = 'STUB_RESPONSE'
    notes = 'this is a placeholder for now'

# load dataset, get sample_id, intent_id of each valid row
    with open(input_path, 'r', encoding= 'utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
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

# Get information of register, phenomena, query
## register
                register = obj.get('register', 'unknown').lower().strip()
                if register not in {'formal', 'informal'}:
                    continue
## phenomena
                phenomena_list = []
                raw_phenomena = obj.get('phenomena', [])
                for p in raw_phenomena:
                    clean_p = str(p).lower().strip()
                    if clean_p not in valid_phenomena:
                        continue
                    phenomena_list.append(clean_p)
## query
                query = obj.get('query', 'unknown').strip()

# compile a result dict for the current row
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
                print(f'Row {line_num} is skipped')

# generate summary, save to output_path
    summary = {
        'total': total,
        'model_name': model_name,
        'results': results
    }

    with open(output_path, 'w', encoding= 'utf-8') as f:
        json.dump(summary, f, indent= 2)

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] in ('-h', '--help'):
        print('Usage: python src/run_model_stub.py <input_jsonl> --out <output_path>')
        sys.exit(0)

    if len(sys.argv) != 4 or sys.argv[2] != '--out':
        print('Usage: python src/run_model_stub.py <input_jsonl> --out <output_path>')
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[3]
    main(input_path, output_path)    