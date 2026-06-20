# Run Eval Pipeline

Runs the evaluator tests against the spam classification pipeline.

```bash
cd /Users/rishavacharya/Desktop/gmail_agent && python -m pytest tests/test_evaluator.py -v
```

After running, report:
- How many tests passed / failed / errored
- Full output for any failures
- Whether `data/agent_log.jsonl` has new entries (indicates real classification ran)
- If `data/spam_examples.jsonl` is missing or empty, note that few-shot examples are needed for meaningful results
