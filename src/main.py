import json
import sys
from collections import Counter

def main(path):
    total = 0
    register_counter = Counter()
    phenomena_counter = Counter()
    intent_counter = Counter()

# Load JSONL data into memory
    with open(path, "r", encoding="utf-8") as f:
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


# Print summary to console
    print("=== Basic Stats ===")
    print(f"Total records: {total}")
    print("By register:", dict(register_counter))
    print("By phenomena:", dict(phenomena_counter))
    print("By intent_id:", dict(intent_counter))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/main.py <input_jsonl>")
        sys.exit(1)

    input_path = sys.argv[1]
    main(input_path)
