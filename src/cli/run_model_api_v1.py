import json
import time
import os
import argparse
from google import genai

parser = argparse.ArgumentParser(
    description='Run Gemini API on a JSONL dataset and save responses.'
)
parser.add_argument(
    '-i', '--in_jsonl',
    default='data/dataset_constraint_sensitive_tiny.jsonl',
    help='Path to input JSONL dataset'
)
parser.add_argument(
    '-o', '--out',
    default='outputs/after_api/run_api_constraint_sensitive_pilot_v0.json',
    help='Path to output JSON summary'
)

def call_model_api(prompt: str) -> str:
    """
    Call Gemini Developer API and return plain text output.
    Includes minimal retry/backoff for transient errors and rate limits.
    """
    client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

    model  = 'gemini-2.5-flash'

    max_attempts = 8
    delay_s = 5.0

    for attempt in range(1, max_attempts + 1):
        try:
            resp = client.models.generate_content(
                model=model,
                contents=prompt
            )
            return (resp.text or '').strip()

        except Exception as e:
            if attempt == max_attempts:
                raise
            time.sleep(delay_s)
            delay_s *= 2


def main():
    args = parser.parse_args()
    input_path = args.in_jsonl
    output_path = args.out
    print('Input path:', input_path)
    print('Output path:', output_path)

    total = 0
    results = {}

    valid_phenomena = {'abbreviation', 'dialect_word', 'informal_lexicon', 'noncanonical_syntax', 'typo'}

    # Placeholders to be replaced/updated on Day 13
    model_name = 'gemini-2.5-flash'
    notes = 'Gemini API call; tiny run; free tier quota constraints.'

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
                time.sleep(13)

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
    print('Total samples processed:', total)

if __name__ == '__main__':
    main()