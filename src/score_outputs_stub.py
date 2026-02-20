import sys, json

# define the 12 rubric items
rubric_items = ['intent_understanding','task_alignment','no_hallucinated_constraints','slot_entity_correctness','no_distort_entities','robustness_to_nonstandard_forms','no_overcorrection_nonstandard_forms','no_harm_unsafe','no_inappropriate_irrelevant','fluency','clear_coherent','conciseness']
def main(input_path, output_path):

# read in data from run_model_stub.py
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    input_ds = data.get('results', {})
    model_name = data.get('model_name', 'unknown')

    results = {}
    for sample_key, sample in input_ds.items():
        sample_id = sample.get('id')
        intent_id = sample.get('intent_id')
        register = sample.get('register')
        phenomena = sample.get('phenomena',[])
        query = sample.get('query')
# define an empty dict for rubric scores for the current sample
        rubric_scores = {}
# placeholder for getting rubric scores
        for item in rubric_items:
            rubric_scores[item] = None
        error_labels = ['placeholder']
        notes = 'this is a placeholder for now'
# compile results
        results[sample_id] = {
            'id':sample_id,
            'intent_id': intent_id,
            'register': register,
            'phenomena': phenomena,
            'query':query,
            'rubric_scores':rubric_scores,
            'error_labels':list(error_labels),
            'notes':notes
        }
# compile summary
    summary = {
        'total':len(results),
        'model_name': model_name,
        'results': results
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] in ('-h', '--help'):
        print('Usage: python src/score_outputs_stub.py <input_json> --out <output_path>')
        sys.exit(0)

    if len(sys.argv) != 4 or sys.argv[2] != '--out':
        print('Usage: python src/score_outputs_stub.py <input_json> --out <output_path>')
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[3]
    main(input_path, output_path)   