# Crypto Price Snapshot & Alert Tool

## What this script does
This script pulls live cryptocurrency prices from a public API, stores them in a structured CSV file, and generates a simple summary report. It also checks basic price thresholds and flags alerts when prices move above or below predefined levels.

The goal is to demonstrate clean data collection, normalisation, and reporting using lightweight Python automation.

---

## API used
- **CoinGecko API**  
  Free, public API (no API key required)

---

## Input → Output

### Input
- A predefined list of cryptocurrency IDs (e.g. bitcoin, ethereum)
- Optional price alert thresholds defined in the script

### Output
- `crypto_prices.csv`  
  Clean snapshot of current prices and 24h change
- `summary.txt`  
  Human-readable summary including triggered alerts

---

## How to run

1. Install requirements:
   ```bash
   pip install requests
2. Run the script:
   ```bash
   python crypto_price_monitor.py
3. Output files will be saved in the output/ folder.
