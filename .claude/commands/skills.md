# Project Skills

List all available custom slash commands for this project.

---

## /test
Runs the full pytest suite (`tests/`) and reports pass/fail with output for any failures.

## /run
Builds and starts the full Docker stack. Checks Flask startup and APScheduler job registration.

## /authorize
Triggers the OAuth2 flow and confirms `gmail/token.json` was written.

## /eval
Runs only the evaluator tests (`tests/test_evaluator.py`) against the spam classification pipeline.

## /check-agent
Smoke-tests the agent by hitting `/retrieveEmails` and validating the JSON response.

## /skills
Shows this list.
