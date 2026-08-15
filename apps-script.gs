/**
 * Google Sheets Weekly Monitor
 *
 * Checks if cells H6:H21 are all empty.
 * If empty, fills B41:B42, D41:D42, F41:F42 with "Zhansaya Z."
 *
 * Setup: Paste this into Google Sheets > Extensions > Apps Script
 * Schedule: Set a time-driven trigger for every Sunday at 10PM
 */

// ── Configuration ──────────────────────────────────────────────────────
const SHEET_NAME = "TENNIS";
const SOURCE_CELLS = ["H6","H7","H8","H9","H10","H11","H12","H13","H14","H15","H16","H17","H18","H19","H20","H21"];
const TARGET_CELLS = ["B41","B42","D41","D42","F41","F42"];
const FILL_VALUE = "Zhansaya Z.";

// ── Main function ──────────────────────────────────────────────────────
function checkAndFill() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);

  if (!sheet) {
    Logger.log("Error: Sheet '" + SHEET_NAME + "' not found.");
    return;
  }

  // Check if ALL source cells are empty
  const allEmpty = SOURCE_CELLS.every(cell => {
    const value = sheet.getRange(cell).getValue();
    return !value || String(value).trim() === "";
  });

  if (allEmpty) {
    // Fill target cells
    TARGET_CELLS.forEach(cell => {
      sheet.getRange(cell).setValue(FILL_VALUE);
    });
    Logger.log("Source cells empty. Filled target cells with '" + FILL_VALUE + "'");
  } else {
    Logger.log("Source cells have data. No action taken.");
  }
}

// ── Setup function (run once) ──────────────────────────────────────────
function setupWeeklyTrigger() {
  // Delete existing triggers first
  ScriptApp.getProjectTriggers().forEach(trigger => {
    if (trigger.getHandlerFunction() === "checkAndFill") {
      ScriptApp.deleteTrigger(trigger);
    }
  });

  // Create new weekly trigger — every Sunday at 10PM
  ScriptApp.newTrigger("checkAndFill")
    .timeBased()
    .onWeekDay(ScriptApp.WeekDay.SUNDAY)
    .atHour(22)
    .create();

  Logger.log("Weekly trigger created: Every Sunday at 10PM");
}
