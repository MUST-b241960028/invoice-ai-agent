"""
Run the invoice agent against the bundled eval_agent dataset.

Usage:
    ANTHROPIC_API_KEY=sk-ant-... python evaluate_eval_agent.py
"""

import argparse
import json
from pathlib import Path

from pipeline import answer_aggregate_questions, process_all_invoices


def main():
    parser = argparse.ArgumentParser(description="Evaluate the invoice agent on eval_agent invoices.")
    parser.add_argument(
        "--data-dir",
        default="dataset/eval_agent/eval_agent",
        help="Directory containing invoice_*.jpg/png/pdf files.",
    )
    parser.add_argument(
        "--db-path",
        default="master_invoices_database.db",
        help="SQLite master database path.",
    )
    parser.add_argument(
        "--output",
        default="eval_agent_results.json",
        help="Where to write evaluation results.",
    )
    args = parser.parse_args()

    results = process_all_invoices(args.data_dir, args.db_path)
    summary = answer_aggregate_questions(results)
    output = {"results": results, "summary": summary}

    Path(args.output).write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    print("Evaluation complete")
    print(f"Total invoices: {summary['total_invoices']}")
    print(f"AUTO_POST: {summary['auto_post_count']}")
    print(f"HUMAN_APPROVAL: {summary['human_approval_count']}")
    print(f"DENY: {summary['deny_count']}")
    print(f"Results written to: {args.output}")


if __name__ == "__main__":
    main()
