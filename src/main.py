import json
import sys
from collections import Counter, defaultdict
# print("I am:", __name__)

def main(input_path, output_path):
    # Reads a JSONL dataset and computes basic stats + intent-level pairing checks
    total = 0
    register_counter = Counter()
    phenomena_counter = Counter()
    # intent_counter = Counter()
    intent_register = defaultdict(Counter)

# Load JSONL data
    with open(input_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f,1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
        
            try:
                obj = json.loads(line)

                total += 1
# Compute basic stats by register, phenomena, and load register counters into intent_register
                register = obj.get('register', 'unknown').lower().strip()
                if register not in {'formal', 'informal'}:
                    continue
                
                register_counter[register] += 1

                for p in obj.get('phenomena', []):
                    clean_p = str(p).lower().strip()
                    if clean_p not in {'abbreviation', 'dialect_word', 'informal_lexicon', 'noncanonical_syntax', 'typo'}:
                        continue
                    phenomena_counter[clean_p] += 1
            
                intent_id = obj.get('intent_id', 'unknown').lower().strip()
                if intent_id != 'unknown':
                    intent_register[intent_id][register] += 1

            except json.JSONDecodeError:
                print(f'Row {line_num} is skipped')

# examine for each intent_id, whether both formal and informal records are available
    bad_pairing_report = {}
    num_bad_pairings = 0
    for intent, counts in intent_register.items():
        missing = list({'formal','informal'} - set(counts.keys()))
        # is_paired = not missing # if missing == [], which is False, is_paired is not Faluse so is True; wait but what if there is a typo?
        is_paired = (counts.get('formal',0) > 0 ) and (counts.get('informal', 0) > 0)

        if not is_paired:
            num_bad_pairings += 1
            note = None
            if 'formal' in missing:
                note = 'missing formal variant'
            elif 'informal' in missing:
                note = 'missing informal variant'
            else:
                note = 'unexpected pairing state'
            bad_pairing_report[intent] = {
                # 'is_paired': is_paired,
                # 'details': dict(counts), # I comment this line only because it makes the output a bit too long
                'missing': missing,
                'note': note
            }

# generate summary, save to output_path
    summary = {
        'total': total,
        'by_register': dict(register_counter),
        'by_phenomena': dict(phenomena_counter),
        # "by_intent_id": dict(intent_counter)
        'num_bad_pairings': num_bad_pairings,
        'bad_pairing_analysis': bad_pairing_report
    }

    with open(output_path, 'w', encoding= 'utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2, sort_keys=False)

if __name__ == '__main__': # when this script is called from CLI directly
    if len(sys.argv) == 2 and sys.argv[1] in ('-h', '--help'):
        print('Usage: python src/main.py <input_jsonl> --out <output_path>')
        sys.exit(0)

    if len(sys.argv) != 4 or sys.argv[2] != '--out':
        print('Usage: python src/main.py <input_jsonl> --out <output_path>')
        sys.exit(1)


    input_path = sys.argv[1]
    output_path = sys.argv[3]
    main(input_path, output_path)


