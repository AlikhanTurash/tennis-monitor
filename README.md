# Tennis Script — Google Sheets Monitor

Monitors a Google Sheet: when cells `H6:H21` are all empty, it fills `B41:B42`, `D41:D42`, `F41:F42` with "Zhansaya Z.".

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Place your `credentials.json` (OAuth2 client) in this directory.

3. Run:
   ```bash
   python monitor.py
   ```

4. First run opens a browser — log in with your Google account to authorize access.

## How it works

- Checks `H6:H21` every 30 seconds
- If all 16 cells are empty → writes "Zhansaya Z." to the 6 target cells
- Ctrl+C to stop
