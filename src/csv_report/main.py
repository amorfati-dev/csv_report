"""Main module for the CSV report generator."""

import argparse
from pathlib import Path

from .load import load_csv
from .report.generate import generate_report, save_report


def parse_args(args=None):
    """Parse command line arguments.

    Args:
        args: List of command line arguments. If None, uses sys.argv.

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Generate a report from a CSV file and optionally email it."
    )
    parser.add_argument(
        "--csv-file", help="Path to the CSV file to analyze", type=str, default=None
    )
    parser.add_argument(
        "--output-format",
        help="Format of the output report (markdown or html)",
        type=str,
        choices=["markdown", "html"],
        default="markdown",
    )
    return parser.parse_args(args)


def main():
    """Main entry point for the application."""
    try:
        # Parse arguments
        args = parse_args()

        # Load data
        df = load_csv(csv_file=args.csv_file)

        # Generate report
        report = generate_report(df)

        # Save report
        output_file = save_report(
            report, Path(f"reports/sp500_analysis.{args.output_format}")
        )
        print(f"Report generated and saved to: {output_file}")

    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()
