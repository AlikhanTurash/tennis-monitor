#!/usr/bin/env python3
"""Google Sheets Weekly Check.

TEST MODE: When B6 is empty → populate B8 with "Zhansaya Z."
PROD MODE: When H6:H21 are empty → populate B41:B42, D41:D42, F41:F42.

Usage:
  python3 monitor.py          # run once and exit (for scheduled execution)
  python3 monitor.py --wait   # keep checking until source empties, then fill and exit
  python3 monitor.py --loop   # run continuously forever (for local testing)
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime

import gspread
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# ── Config ──────────────────────────────────────────────────────────────
SPREADSHEET_ID = "1WXNZsK5Atb-VSjfahnCeay388ZOCmb02HrA0pP0zf3A"
SHEET_NAME = "TENNIS"

# TEST MODE — change to production values when ready
SOURCE_CELLS = ["B6"]
TARGET_CELLS = ["B8"]

# PROD MODE (uncomment when ready):
# SOURCE_CELLS = ["H6","H7","H8","H9","H10","H11","H12","H13","H14","H15","H16","H17","H18","H19","H20","H21"]
# TARGET_CELLS = ["B41","B42","D41","D42","F41","F42"]

FILL_VALUE = "Zhansaya Z."
POLL_INTERVAL = 5  # seconds (only used in --loop mode)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDENTIALS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "credentials.json")
TOKEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "token.json")


# ── Auth ────────────────────────────────────────────────────────────────
def authenticate() -> Credentials:
    """Handle OAuth2 — supports both local and GitHub Actions (env var)."""
    creds = None

    # GitHub Actions: credentials from environment variable
    creds_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
    if creds_json:
        creds_dict = json.loads(creds_json)
        creds = Credentials.from_authorized_user_info(creds_dict, SCOPES)
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
        return creds

    # Local: credentials from file
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...", flush=True)
            creds.refresh(Request())
        else:
            print("Opening browser for Google login...", flush=True)
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
        print("Token saved to token.json", flush=True)

    return creds


# ── Sheet helpers ───────────────────────────────────────────────────────
def get_sheet(creds: Credentials) -> gspread.Worksheet:
    """Open the specific worksheet by name."""
    print("Connecting to Google Sheets...", flush=True)
    gc = gspread.authorize(creds)
    spreadsheet = gc.open_by_key(SPREADSHEET_ID)
    ws = spreadsheet.worksheet(SHEET_NAME)
    return ws


def check_source_empty(ws: gspread.Worksheet) -> bool:
    """Return True if ALL source cells are empty."""
    for cell in SOURCE_CELLS:
        value = ws.acell(cell).value
        if value and str(value).strip():
            return False
    return True


def populate_target(ws: gspread.Worksheet) -> None:
    """Write FILL_VALUE to every target cell."""
    for cell in TARGET_CELLS:
        ws.update_acell(cell, FILL_VALUE)


# ── Main logic ──────────────────────────────────────────────────────────
def run_once(ws: gspread.Worksheet) -> None:
    """Single check: if source empty, fill targets. Then exit."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    source = ', '.join(SOURCE_CELLS)
    if check_source_empty(ws):
        print(f"[{now}] {source} is empty — filling target cells...", flush=True)
        populate_target(ws)
        print(f"[{now}] Done. Filled: {', '.join(TARGET_CELLS)}", flush=True)
    else:
        print(f"[{now}] {source} has data — no action needed.", flush=True)


def run_wait(ws: gspread.Worksheet) -> None:
    """Keep checking until source cells are empty, then fill and exit."""
    source = ', '.join(SOURCE_CELLS)
    print(f"Waiting for {source} to be emptied — poll interval {POLL_INTERVAL}s", flush=True)
    print(f"Target cells: {', '.join(TARGET_CELLS)}", flush=True)
    print("Press Ctrl+C to stop.\n", flush=True)

    while True:
        now = datetime.now().strftime("%H:%M:%S")

        if check_source_empty(ws):
            print(f"[{now}] {source} is empty — filling target cells...", flush=True)
            populate_target(ws)
            print(f"[{now}] Done. Filled: {', '.join(TARGET_CELLS)}", flush=True)
            break
        else:
            print(f"[{now}] {source} has data — waiting...", flush=True)

        time.sleep(POLL_INTERVAL)


def run_loop(ws: gspread.Worksheet) -> None:
    """Continuous monitoring loop (for local testing). Runs forever."""
    source = ', '.join(SOURCE_CELLS)
    print(f"Monitoring {source} — poll interval {POLL_INTERVAL}s", flush=True)
    print(f"Target cells: {', '.join(TARGET_CELLS)}", flush=True)
    print("Press Ctrl+C to stop.\n", flush=True)

    while True:
        now = datetime.now().strftime("%H:%M:%S")

        if check_source_empty(ws):
            print(f"[{now}] {source} is empty — populating target cells...", flush=True)
            populate_target(ws)
            print(f"[{now}] Done.", flush=True)
        else:
            print(f"[{now}] {source} has data — waiting...", flush=True)

        time.sleep(POLL_INTERVAL)


# ── Entry point ─────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(description="Google Sheets weekly check")
    parser.add_argument("--loop", action="store_true", help="Run continuously (for testing)")
    parser.add_argument("--wait", action="store_true", help="Wait for source to empty, then fill and exit")
    args = parser.parse_args()

    try:
        creds = authenticate()
        ws = get_sheet(creds)
        print(f"Connected to sheet: {ws.title}\n", flush=True)

        if args.wait:
            run_wait(ws)
        elif args.loop:
            run_loop(ws)
        else:
            run_once(ws)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr, flush=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
