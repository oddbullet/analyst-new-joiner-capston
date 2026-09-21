import argparse
import json
import sys

from src.meridian.graph import run_graph


def main() -> None:
    parser = argparse.ArgumentParser(description="Classify a support ticket via the LangGraph pipeline.")
    parser.add_argument("text", nargs="?", help="Ticket text. If omitted, reads from stdin.")
    args = parser.parse_args()

    text = args.text if args.text is not None else sys.stdin.read()

    result = run_graph(text)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
