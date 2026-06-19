# Project Skills

List all available custom slash commands for this project.

---

## /test
Runs the full pytest suite (`tests/`) and reports pass/fail with output for any failures.

```bash
python -m pytest tests/ -v
```

## /skills
Shows this list.

---

## Useful one-liners (not skills, but handy)

```bash
# Start the app
docker compose up --build

# Trigger OAuth and first email read
curl http://localhost:5000/authorize

# Fetch emails as JSON
curl http://localhost:5000/retrieveEmails
```
