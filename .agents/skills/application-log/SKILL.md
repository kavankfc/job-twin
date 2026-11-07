---
name: application-log
description: Create or update the private data/application_log.csv for job applications. Use whenever adding a new application, recording a status change (drafted/submitted/interview/rejected/withdrawn/accepted), or maintaining application history.
---

# Application Log

`data/application_log.csv` is a private long-format status history (versioned only in the private `data/` repo). Exact header:

```csv
date,application_id,company_name,company_sector,role_name,application_status,note
```

One row per status event, so the same `application_id` appears on multiple rows as the application progresses. Exception: a repeated `drafted` event for the same company and role updates the existing drafted row's `date` only, preserving all its other fields.

## Update Procedure

1. Create the file with the header if missing; read existing rows with CSV-aware handling.
2. Match `company_name` + `role_name` case-insensitively (trimmed). On a match, reuse the first matching row's `application_id`, `company_name`, `company_sector`, and `role_name` exactly — even if the new event is in a later month.
3. No match: assign the next ID as `APP-YYYYMM-NNN`, where `YYYYMM` is the event month and `NNN` the next sequence number for that month.
4. Append the new status row (or update the drafted row's date per the exception). Never overwrite history otherwise, unless the user explicitly asks to correct an error.
5. Sort rows by `date` descending and save.

## Field Rules

- `date`: `YYYY-MM-DD`.
- `company_name` / `role_name`: canonical names.
- `company_sector`: broad sector (`Utilities`, `Financial Services`, `Insurance`, `Real Estate`, `Technology`, …); `Unknown` if unknown for a new application; copy the existing sector for known applications.
- `note`: user-provided text only — never invent notes, details, links, or context.

Before finishing, confirm the header is exact, IDs/fields are reused consistently, rows are sorted by date descending, and the CSV parses.
