"""Main entry point for the CSV report generator."""
from __future__ import annotations

import pandas as pd
from pathlib import Path
import argparse
import sys
from csv_report.load import DataLoadError, load_csv, get_default_csv_path
from csv_report.report.compute import compute_all_kpis
from csv_report.report.generate import generate_report, save_report



def send_email(to: str, subject: str, body: str) -> None:
    """Send an email with the report."""
    print("[EMAIL]")
    print(f"To     : {to}")
    print(f"Subject: {subject}")
    print("Body   :\n" + body)

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate a report from a CSV file and optionally email it.")

    parser.add_argument(
    "--csv", "-c",
    default=str(get_default_csv_path()),
    help="Path or URL to CSV (default: %(default)s)"
)

    parser.add_argument(
        "--email", "-e",
        help="Email address to receive the report")

    parser.add_argument(
        "--subject", "-s",
        default="CSV Report",
        help="Subject line for the email")

    return parser.parse_args()

def main() -> None:
    """Main entry point."""
    args = parse_args()
    
    try:
        # Load and analyze the data
        df = load_csv(args.csv)
        
        # Generate report
        report_body = (
            f"Report for S&P 500 Companies\n"
            "-------------------------------------------\n"
            f"Total Companies: {len(df)}\n"
            f"Top Companies:\n{df[['Symbol', 'Shortname', 'Marketcap']].head()}\n"
            f"Sector Distribution:\n{df['Sector'].value_counts().head()}"
        )

        # Send or print report
        if args.email:
            send_email(args.email, args.subject, report_body)
        else:
            print(report_body)
            
    except DataLoadError as e:
        print(f"Error loading data: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

