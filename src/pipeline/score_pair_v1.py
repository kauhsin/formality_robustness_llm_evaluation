import argparse
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description='Score pipeline: scores_csv -> score_summary + pairing')
    parser.add_argument('--scores_csv', required=True)
    parser.add_argument('--score_out', required=True)
    parser.add_argument('--pair_out', required=True)
    args = parser.parse_args()

    subprocess.run(
        [sys.executable, 'src/cli/score_outputs_v0.py', '--in_csv', args.scores_csv, '--out', args.score_out, '--pair', args.pair_out],
        check=True
    )


if __name__ == '__main__':
    main()