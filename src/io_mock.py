import json, sys
from collections import Counter

def main(input_path, output_path):
    with open(input_path, 'r', encoding = 'utf-8') as f:
        total = 0
        register_counter = Counter()

        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            total += 1
            obj = json.loads(line)
            register = obj.get('register', 'unknown')
            register_counter[register] += 1
        
        summary = {
            'total': total,
            'by_register': dict(register_counter)
        }

        with open(output_path, 'w', encoding= 'utf-8') as f:
            json.dump(summary, f, indent=2)

if __name__ == '__main__':
    if len(sys.argv) < 4 or sys.argv[2] != '--out':
        print('Usage: io_mock.py <input_path> --out <output_path>')
    
    input_path = sys.argv[1]
    output_path = sys.argv[3]
    main(input_path, output_path)