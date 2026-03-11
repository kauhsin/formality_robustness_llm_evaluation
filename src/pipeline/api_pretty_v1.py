import argparse
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description='Infer pipeline: run_api -> pretty_print')
    parser.add_argument('--dataset_jsonl', required=True)
    parser.add_argument('--run_out', required=True)
    parser.add_argument('--pretty_out', required=True)
    args = parser.parse_args()

    subprocess.run(
        [sys.executable, 'src/cli/run_model_api_v1.py', '--in_jsonl', args.dataset_jsonl, '--out', args.run_out],
        check=True
    )

    subprocess.run(
        [sys.executable, 'src/pretty_print_run_model.py', '--in', args.run_out, '--out', args.pretty_out, '--sort-register'],
        check=True
    )


if __name__ == '__main__':
    main()