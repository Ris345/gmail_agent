# Check Agent

Smoke-tests the agent by hitting /retrieveEmails and checking for a valid JSON response. The app must already be running.

```bash
curl -s http://localhost:8080/retrieveEmails | python3 -m json.tool
```

After running, report:
- Whether the response is a valid JSON array of emails
- If the response is an error string or empty, check Flask logs for APScheduler failures or import errors in `Agent/parent_agent.py`
- If the server is unreachable, confirm the Docker stack is up with `docker compose ps`
