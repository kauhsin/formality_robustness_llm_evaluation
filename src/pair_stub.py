import sys, json

def main(input_path, output_path):
    total = 0
# read in data from score_outputs_stub.py (score_XXXXXXXX.json)
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    input_ds = data.get('results', {})
    model_name = data.get('model_name', 'unknown')

    pairs = {}

    for sample in input_ds.values():
        sample_id = sample.get('id')
        intent_id = sample.get('intent_id')
        register = sample.get('register')
        phenomena = sample.get('phenomena',[])
        query = sample.get('query')
        rubric_scores = sample.get('rubric_scores',{})
        error_labels = sample.get('error_labels',[])
        notes = sample.get('notes')

        if not intent_id or intent_id == 'unknown':
            continue
        if register not in ('formal', 'informal'):
            continue

# placeholder for getting response text
        response_text = 'this is a placeholder for now'
# Compile pairs
        if intent_id not in pairs:
            pairs[intent_id] = {}

        pairs[intent_id][register] = {
            'id':sample_id,
            'phenomena': phenomena,
            'query': query,
            'rubric_scores': rubric_scores,
            'error_labels': error_labels,
            'notes': notes,
            'response_text': response_text
        }
# generate pair analysis
    for intent_id in pairs.keys():
        has_formal = 'formal' in pairs[intent_id]
        has_informal = 'informal' in pairs[intent_id]
        pair_complete = has_formal and has_informal

        pair_analysis = {
            'has_formal':has_formal,
            'has_informal':has_informal,
            'pair_complete':pair_complete
        }
        pairs[intent_id]['pair_analysis'] = pair_analysis

# compile summary
    summary = {
        'model_name': model_name,
        'total_pair_num': len(pairs),
        'pairs': pairs
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary,f,indent = 2)

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] in ('-h', '--help'):
        print('Usage: python src/pair_stub.py <input_json> --out <output_path>')
        sys.exit(0)

    if len(sys.argv) != 4 or sys.argv[2] != '--out':
        print('Usage: python src/pair_stub.py <input_json> --out <output_path>')
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[3]
    main(input_path, output_path)   