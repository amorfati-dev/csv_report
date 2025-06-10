# csv_report

Kleines CLI-Tool, das CSV-Daten auswertet und einen Report mailt.

## Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd csv_report
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies in editable mode:
   ```bash
   pip install -e . --break-system-packages
   ```

## Usage

Run the CLI tool with:
```bash
csv_report --csv data/sp500_companies.csv
```

## Requirements
- Python 3.9+
- pandas

## Example Output
```
Report for S&P 500 Companies
-------------------------------------------
Total Companies: 503
Top Companies:
  Symbol              Shortname      Marketcap
0   AAPL             Apple Inc.  3745241628672
1   NVDA     NVIDIA Corporation  3307864588288
2   MSFT  Microsoft Corporation  3296105332736
3   AMZN       Amazon.com, Inc.  2366295506944
4  GOOGL          Alphabet Inc.  2276776214528
Sector Distribution:
Sector
Technology            82
Industrials           70
Financial Services    67
Healthcare            63
Consumer Cyclical     55
Name: count, dtype: int64
```
