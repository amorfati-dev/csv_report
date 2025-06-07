from __future__ import annotations

import pandas as pd
import os
from pathlib import Path
import argparse

#!/usr/bin/env python3
"""csv_report main entry point

Usage example:
    python src/main.py --csv data/sp500_companies.csv --email you@example.com

The script will later generate a summary report from a CSV file and optionally
send it via e‑mail. For now, e‑mail sending is stubbed out. You can extend this
file incrementally: plug in pandas processing, proper HTML/plain‑text e‑mail,
etc.
"""

# ---------------------------------------------------------------------------
# Dummy mail helper – replace with real sending logic later
# ---------------------------------------------------------------------------

def send_email(to: str, subject: str, body: str) -> None:
    """Pretend to send an e‑mail by printing to stdout."""
    print("[EMAIL]")
    print(f"To     : {to}")
    print(f"Subject: {subject}")
    print("Body   :\n" + body)

# ---------------------------------------------------------------------------
# CLI argument handling
# ---------------------------------------------------------------------------

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a quick report from a CSV file and optionally e‑mail it.")

    parser.add_argument(
        "--csv", "-c",
        default=None,
        help="Path to the CSV file (default: data/sp500_companies.csv)")

    parser.add_argument(
        "--email", "-e",
        help="E‑mail address that should receive the report (optional)")

    parser.add_argument(
        "--subject", "-s",
        default="CSV Report",
        help="Subject line for the outgoing e‑mail (default: %(default)s)")

    return parser.parse_args(argv)

# ---------------------------------------------------------------------------
# Main entry
# ---------------------------------------------------------------------------

def main() -> None:
    args = parse_args()
    # Determine CSV path
    if args.csv:
        csv_path = Path(args.csv)
    else:
        script_dir = Path(__file__).parent.parent
        csv_path = script_dir / 'data' / 'sp500_companies.csv'
    
    if not csv_path.exists():
        print(f"⚠️  CSV file '{csv_path}' not found!")
        return
        
    # Read and analyze the data
    df = pd.read_csv(csv_path)
    
    # Basic analysis
    print("\n=== S&P 500 Analysis ===")
    print(f"Total companies: {len(df)}")
    print("\nTop 5 companies by market cap:")
    print(df[['Symbol', 'Shortname', 'Marketcap']].head())
    
    print("\nSector distribution:")
    print(df['Sector'].value_counts().head())

    report_body = (
        f"Report for {csv_path.name} (placeholder).\n"
        "-------------------------------------------\n"
        "This is where your report summary will appear."
    )

    if args.email:
        send_email(args.email, args.subject, report_body)
    else:
        print(report_body)

if __name__ == "__main__":  # pragma: no cover
    main()
