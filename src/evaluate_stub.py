import sys, json

def main(input_path, output_path):
    total = 0
    results = {}
    rubric_scores_report = {}
    error_labels = ['placeholder']
    notes = 'this is a placeholder for now'
    key = ''

# stub
    rubric_scores_report = {
        'intent_understanding': 2,
        'task_alignment': 2,
        'no_hallucinated_constraints': 2,
        'slot_entity_correctness': 2,
        'no_distort_entities': 2,
        'robustness_to_nonstandard_forms': 2,
        'no_overcorrection_nonstandard_forms': 2,
        'no_harm_unsafe': 2,
        'no_inappropriate_irrelevant': 2,
        'fluency': 1,
        'clear_coherent': 1,
        'conciseness': 1
    }
# Load JSONL data
    with open (input_path, 'r', encoding='utf-8') as f:
        for line_num,line in enumerate(f,1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            try:
                obj = json.loads(line)

# Compute rubric_scores report. put in dummy scores for now.
                register = obj.get('register', 'unknown').lower().strip()         
                intent_id = obj.get('intent_id', 'unknown').lower().strip()
                if intent_id != 'unknown' and ((register == 'formal') or (register == 'informal')):
                    total += 1
# replace placeholders later                    
                    key = f'{intent_id}_{register}'
                    results[key] = {
                        'intent_id': intent_id,
                        'register': register,
                        'rubric_scores': dict(rubric_scores_report),
                        'error_labels': list(error_labels),
                        'notes': notes
                    }

            except json.JSONDecodeError:
                print(f'Row {line_num} is skipped')

# generate summary, save to output_path


# generate summary, save to output_path
    summary= {
        'total': total,
        'model_name': 'placeholder_model',
        'result': results
    }

    with open(output_path, 'w', encoding= 'utf-8') as f:
        json.dump(summary, f, indent=2)



if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] in ('-h', '--help'):
        print('Usage: python src/evaluate_stub.py <input_jsonl> --out <output_path>')
        sys.exit(0)

    if len(sys.argv) != 4 or sys.argv[2] != '--out':
        print('Usage: python src/evaluate_stub.py <input_jsonl> --out <output_path>')
        sys.exit(1)


    input_path = sys.argv[1]
    output_path = sys.argv[3]
    main(input_path, output_path)    