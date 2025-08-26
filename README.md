# CrowdWisdomTrading AI Agent — Internship Assessment

CLI project using CrewAI-style flow, guardrails, and litellm. Produces per-user sentiment,
tickers, and a PDF report. Works offline in mock mode; with keys it uses litellm.

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py --usernames-file samples/sample_usernames.txt --outdir outputs/mock_run
# with LLM:
# python main.py --usernames-file samples/sample_usernames.txt --outdir outputs/llm_run --use-llm
```

Outputs:
- Per-user JSON: `outdir/json/*.json`
- Consolidated: `outdir/summary.json`
- Report: `outdir/report.pdf`

No server or ports used (CLI only).