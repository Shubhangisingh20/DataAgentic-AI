# Data Agent

A multi-agent data assistant built with [LangGraph](https://github.com/langchain-ai/langgraph). A router classifies each natural-language request as either a **SQL** question or an **ETL** task, then hands it off to a specialized sub-agent.

## Architecture

```
            ┌──────────────┐
  user  ──▶ │ router_node  │
            └──────┬───────┘
                    │
         ┌──────────┴──────────┐
         ▼                     ▼
 ┌───────────────┐     ┌───────────────┐
 │  sql_analyst   │     │  etl_analyst   │
 └───────────────┘     └───────────────┘
```

- **`sql_analyst`** — curates the user's question, pulls live schema + sample data from Postgres, generates a SQL query with an LLM, runs a second LLM pass as a safety judge (blocks anything beyond read-only `SELECT`), executes the query, and summarizes the result in plain language.
- **`etl_analyst`** — a tool-using agent that can pull data from an API into CSV/JSON/Parquet, or transform an existing file with LLM-generated Pandas code.

Graph diagrams are checked in as `data_agent_graph.png`, `sql_analyst_graph.png`, and `etl_analyst_graph.png`.

## Setup

Requires [uv](https://docs.astral.sh/uv/) and a local Postgres instance.

```bash
uv sync
cp .env.example .env   # then fill in your own values
```

`.env` variables:

| Variable | Purpose |
|---|---|
| `GROQ_API_KEY` | LLM calls (via `langchain-groq`) |
| `host`, `port`, `database`, `user`, `password` | Postgres connection |

Seed the database with the sample ride-share dataset in `Data/` (synthetic data — no real users):

```bash
uv run python feed_db.py
```

## Running

```bash
uv run python -m Agents.data_agent
```

Or run either sub-agent directly:

```bash
uv run python -m Agents.sql_analyst
uv run python -m Agents.etl_analyst
```

## Known limitations

- `ETLTools.execute_code` (`Utils/etl_tools.py`) runs LLM-generated Pandas code via a raw `exec()` with no sandboxing. Fine for a local demo against trusted data; would need a sandboxed execution environment (e.g. a restricted subprocess, `RestrictedPython`, or a container) before handling untrusted input.
- The SQL safety judge is an LLM call, not a hard guarantee — `is_safe_sql` is a second line of defense, not a substitute for running the DB user with read-only grants.
- Postgres connection is local-only (`host=localhost`); there's no deployed/hosted database behind this yet.
