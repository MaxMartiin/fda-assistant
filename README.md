# fda-assistant

A regulatory Q&A assistant over public FDA data, built in stages. It's the final project for my [LLM learning log](https://github.com/MaxMartiin/LLM-Learning).

## Status
- [x] Part 1: Streaming API with cost and latency logging
- [ ] Part 2: FDA data ingestion and cleaning (openFDA + guidance PDFs)
- [ ] Part 3: Answers grounded in FDA documents, with citations (RAG + pgvector)
- [ ] Part 4: Agent with tools

## How it works
`client.py` → `POST /ask` → FastAPI streams Claude's answer as it's generated → when the stream ends, it logs tokens, time to first text, total time, cost, and stop reason to Postgres (Neon).

## Design decisions
- **Streaming:** the first words appear in under a second instead of after the full answer is done.
- **Async, with the database write on a separate thread:** a slow write doesn't freeze other requests.
- **Logs prompt length, not prompt text:** a habit for sensitive data such as patient information.
- **Flags cut-off answers** when `stop_reason` is `max_tokens`, including when the model spends its whole budget thinking.
- **Only `ttft_s` can be NULL** (no text was produced). Every other column is required, so bad inserts fail loudly.

## Sample log
| input | output | ttft_s | total_s | cost_usd | stop_reason |
|---|---|---|---|---|---|
| 20 | 198 | 0.85 | 1.50 | $0.000101 | end_turn |
| 21 | 50 | NULL | 0.96 | $0.000027 | max_tokens |

## Known limitations
- Prices are hardcoded for Claude Haiku 5.5 (prompts up to 100K tokens).
- If the API errors or the client disconnects mid-stream, the request isn't logged.
- The model answers from its training data, which can be out of date. In testing it listed CFSAN, which was reorganized into the FDA's Human Foods Program in October 2024. Part 3 fixes this.

## Run it
```
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
Create `.env` with:
```
ANTHROPIC_API_KEY=...
DATABASE_URL=postgresql+psycopg://...
```
Then run:
```
fastapi dev main.py
python client.py
```