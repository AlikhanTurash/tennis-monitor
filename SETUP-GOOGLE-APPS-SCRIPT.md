# Setup Guide — Google Apps Script

## Step 1: Open Apps Script

1. Open your Google Sheet: [SPORT FIELDS SPRING 2026](https://docs.google.com/spreadsheets/d/1WXNZsK5Atb-VSjfahnCeay388ZOCmb02HrA0pP0zf3A)
2. Go to **Extensions** → **Apps Script**
3. Delete any default code in the editor

## Step 2: Paste the Script

1. Open the file `apps-script.gs` (in this folder)
2. Copy ALL the code
3. Paste it into the Apps Script editor
4. Click the **Save** icon (💾)

## Step 3: Set Up the Weekly Trigger

1. In Apps Script, find and run the function `setupWeeklyTrigger`
   - Click the function dropdown (next to the Run button)
   - Select `setupWeeklyTrigger`
   - Click **Run**
2. Authorize when prompted (click through the permissions)

That's it! The script will now run automatically every Sunday at 10PM.

## How to Test Manually

1. In Apps Script, select `checkAndFill` from the function dropdown
2. Click **Run**
3. Check the **Execution log** at the bottom for results

## How to Check Logs

1. In Apps Script, click **Executions** (clock icon in left sidebar)
2. See when the script ran and what it did

## How to Disable

1. In Apps Script, click **Triggers** (clock icon in left sidebar)
2. Find the `checkAndFill` trigger
3. Click the three dots → **Delete trigger**
