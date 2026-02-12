import json
import sys
from collections import Counter
# print("I am:", __name__)

def main(input_path, output_path):
    total = 0
    register_counter = Counter()
    phenomena_counter = Counter()
    intent_counter = Counter()

# Load JSONL data into memory
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            obj = json.loads(line)

            total += 1
# Compute basic stats by register, phenomena, and intent_id
            register = obj.get("register", "unknown")
            register_counter[register] += 1

            for p in obj.get("phenomena", []):
                phenomena_counter[p] += 1
            
            intent_id = obj.get("intent_id", "unknown")
            intent_counter[intent_id] += 1


# generate summary, save to output_path
    summary = {
        "total": total,
        "by_register": dict(register_counter),
        "by_phenomena": dict(phenomena_counter),
        # "by_intent_id": dict(intent_counter)
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2, sort_keys=True)

if __name__ == "__main__": # when this script is called from CLI directly
    if len(sys.argv) == 2 and sys.argv[1] in ("-h", "--help"):
        print("Usage: python src/main.py <input_jsonl> --out <output_path>")
        sys.exit(0)

    if len(sys.argv) != 4 or sys.argv[2] != "--out":
        print("Usage: python src/main.py <input_jsonl> --out <output_path>")
        sys.exit(1)


    input_path = sys.argv[1]
    output_path = sys.argv[3]
    main(input_path, output_path)


