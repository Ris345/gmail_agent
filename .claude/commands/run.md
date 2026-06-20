# Run App

Builds and starts the full Docker stack.

```bash
cd /Users/rishavacharya/Desktop/gmail_agent && docker compose up --build
```

After running, report:
- Whether Flask logged `Running on http://0.0.0.0:5001`
- Whether APScheduler logged the 3-day job registration
- Any startup errors (import failures, missing env vars, port conflicts)
