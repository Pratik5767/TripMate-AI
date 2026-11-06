<div align="center">

# ✈️ TripMate AI

**A multi-agent travel planner built with LangGraph, FastAPI and Groq.**
Describe a trip in plain English and get flights, hotels and a day-by-day itinerary in one structured plan.

<br>

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?logo=langchain&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-F55036)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[Overview](#-overview) · [Features](#-features) · [How it works](#-how-it-works) · [Getting started](#-getting-started) · [API](#-api-reference) · [Limitations](#-limitations) · [Roadmap](#-roadmap)

</div>

<!--
  Add a screenshot of the app here once you have one:

  <p align="center"><img src="docs/screenshot.png" alt="TripMate AI interface" width="85%"></p>
-->

---

## 📖 Overview

TripMate AI turns a single sentence such as _"Plan a complete 7 days Japan trip from Bangladesh including flights, hotels and sightseeing under 2 lakhs"_ into a complete, readable travel plan.

Behind the scenes, a **LangGraph** workflow passes your request through four specialised agents. Each one adds a piece of the plan: flight information, hotel research, an itinerary draft and a final formatted answer. Conversation state is saved in **PostgreSQL**, so a trip thread can be resumed later. The result is served through a **FastAPI** backend and a lightweight web interface, with one-click copy and PDF export.

## ✨ Features

- **Multi-agent pipeline.** Four focused agents run in sequence on a LangGraph state graph.
- **Natural-language route parsing.** Understands phrases like _"from Dhaka to Tokyo"_, plain IATA codes (`DAC to NRT`), or just a destination.
- **City and country to airport resolution.** Maps place names to airport codes using a curated lookup table, with `airportsdata` and `pycountry` as fallbacks.
- **Live flight data** from the AviationStack API, including airline, flight number, status, terminals, gates and delays.
- **Hotel research** through Tavily web search, with titles, links and short snippets passed to the planner.
- **Persistent conversation threads.** State is checkpointed to PostgreSQL through LangGraph's `PostgresSaver`, and the browser remembers your thread ID.
- **Structured, readable output** with trip summary, flights, hotels, day-by-day itinerary, estimated budget and recommendations, rendered from Markdown.
- **Export tools.** Copy the plan to the clipboard or download it as a PDF.
- **Keyboard shortcut.** Press `Ctrl + Enter` to generate a plan.
- **Health endpoint and auto-generated API docs** (`/health`, `/docs`).

## 🧠 How it works

```mermaid
flowchart LR
    U([User request]) --> F["Flight Agent<br/><sub>AviationStack</sub>"]
    F --> H["Hotel Agent<br/><sub>Tavily search</sub>"]
    H --> I["Itinerary Agent<br/><sub>Groq LLM</sub>"]
    I --> R["Final Response Agent<br/><sub>Groq LLM</sub>"]
    R --> O([Markdown travel plan])
```

All agents share one `TravelState` (messages, user query, flight results, hotel results, itinerary and an `llm_calls` counter). The compiled graph is checkpointed to PostgreSQL after each run.

| Agent                    | Responsibility                                                            | Powered by                  |
| ------------------------ | ------------------------------------------------------------------------- | --------------------------- |
| **Flight Agent**         | Parses the route from the request and fetches matching live flights       | AviationStack API           |
| **Hotel Agent**          | Searches the web for hotels that fit the request                          | Tavily                      |
| **Itinerary Agent**      | Drafts a practical, budget-aware itinerary from the flight and hotel data | Groq (`openai/gpt-oss-20b`) |
| **Final Response Agent** | Produces the formatted answer with summary, budget and recommendations    | Groq (`openai/gpt-oss-20b`) |

## 🧰 Tech stack

| Layer         | Technology                                                                                                              |
| ------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Orchestration | [LangGraph](https://github.com/langchain-ai/langgraph), [LangChain](https://github.com/langchain-ai/langchain)          |
| LLM           | [Groq](https://groq.com) via `langchain-groq`                                                                           |
| Backend       | [FastAPI](https://fastapi.tiangolo.com), Uvicorn, Jinja2                                                                |
| Persistence   | PostgreSQL with `langgraph-checkpoint-postgres`, `psycopg`                                                              |
| Flight data   | [AviationStack](https://aviationstack.com), `airportsdata`, `pycountry`                                                 |
| Web search    | [Tavily](https://tavily.com)                                                                                            |
| Frontend      | HTML, CSS, vanilla JavaScript, [marked](https://marked.js.org), [html2pdf.js](https://github.com/eKoopmans/html2pdf.js) |

## 📁 Project structure

```
TripMate-AI-Multi-Agent-Travel-Planner/
├── app.py                 # FastAPI app: routes, static files, templates
├── backend.py             # LangGraph workflow, LLM setup, PostgreSQL checkpointer
├── test.py                # Command-line smoke test for the agent pipeline
├── requirements.txt       # Python dependencies (pinned)
├── docker-compose.yml     # pgAdmin for inspecting the database locally
├── data/
│   └── airports.py        # City and country to IATA lookup tables
├── tools/
│   ├── flight_tool.py     # Route parsing and AviationStack flight lookup
│   └── tavily_tool.py     # Tavily search used for hotel research
├── templates/
│   └── index.html         # Jinja2 page served at "/"
└── static/
    ├── style.css
    └── script.js          # API calls, Markdown rendering, copy and PDF export
```

## 🚀 Getting started

### Prerequisites

- **Python 3.10 or newer**
- A **PostgreSQL** database (a hosted instance such as Render works, or run one locally)
- API keys for three services:
  - [Groq](https://console.groq.com) for the language model
  - [Tavily](https://tavily.com) for web search
  - [AviationStack](https://aviationstack.com) for flight data

### 1. Clone the repository

```bash
git clone https://github.com/Pratik5767/TripMate-AI-Multi-Agent-Travel-Planner.git
cd TripMate-AI-Multi-Agent-Travel-Planner
```

### 2. Create a virtual environment and install dependencies

```bash
# macOS / Linux
python -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
```

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root (it is already listed in `.gitignore`):

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
AVIATIONSTACK_API_KEY=your_aviationstack_api_key
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Optional: origin airport used when a request names only a destination
DEFAULT_ORIGIN_IATA=PNQ
```

| Variable                | Required | Description                                                                                                 |
| ----------------------- | -------- | ----------------------------------------------------------------------------------------------------------- |
| `GROQ_API_KEY`          | Yes      | Key for the Groq-hosted language model. The app stops at startup if it is missing.                          |
| `TAVILY_API_KEY`        | Yes      | Key for Tavily web search (hotel research).                                                                 |
| `AVIATIONSTACK_API_KEY` | Yes      | Key for live flight data. Without it, the flight step returns an explanatory message instead of results.    |
| `DATABASE_URL`          | Yes      | PostgreSQL connection string used by the LangGraph checkpointer. The app stops at startup if it is missing. |
| `DEFAULT_ORIGIN_IATA`   | No       | Departure airport when only a destination is given. Defaults to `PNQ`.                                      |

> **Note on SSL.** If `DATABASE_URL` has no `sslmode` parameter, the app appends `sslmode=require` automatically. For a local PostgreSQL server without SSL, add `?sslmode=disable` to the URL yourself.

### 4. Run the app

```bash
uvicorn app:app --reload
```

Open **http://127.0.0.1:8000** in your browser. On first start, the checkpointer creates the tables it needs in your database.

You can also start it with `python app.py`, which runs Uvicorn on `127.0.0.1:8000` with auto-reload.

### Optional: test from the command line

```bash
python test.py
```

Enter a travel request when prompted and the final plan prints to the terminal. This is handy for checking your API keys without opening the UI.

### Optional: inspect the database with pgAdmin

```bash
docker compose up -d
```

pgAdmin is then available at **http://localhost:5050**. The default login is defined in `docker-compose.yml`; change those credentials before using it on anything other than your own machine.

## 💬 Usage

Type a request into the planner, or pick one of the quick prompts, then press **Generate Plan** (or `Ctrl + Enter`).

**Example requests**

```text
Plan a complete 7 days Japan trip from Bangladesh including flights, hotels and sightseeing under 2 lakhs.
Plan a 5 days Dubai trip from Dhaka with flights, hotels and sightseeing.
Plan a 7 days Thailand trip from Bangladesh with budget hotels and sightseeing.
Give me all country flight info.
```

**Tips for better results**

- Phrase routes as _"from X to Y"_ so the origin and destination are detected reliably.
- Airport codes work too, for example `DAC to NRT`.
- If you mention only a destination, flights are searched from `DEFAULT_ORIGIN_IATA`.
- Include a budget, trip length and interests to get a more tailored itinerary.

## 🔌 API reference

Interactive documentation is available at `/docs` while the server is running.

### `POST /api/travel`

Generate a travel plan.

**Request body**

| Field       | Type             | Description                                                                               |
| ----------- | ---------------- | ----------------------------------------------------------------------------------------- |
| `message`   | string           | The travel request. Must not be empty.                                                    |
| `thread_id` | string, optional | Reuse a previous thread ID to continue a conversation. A new one is generated if omitted. |

```bash
curl -X POST http://127.0.0.1:8000/api/travel \
  -H "Content-Type: application/json" \
  -d '{"message": "Plan a 5 days Dubai trip from Dhaka with flights, hotels and sightseeing."}'
```

**Successful response**

```json
{
  "success": true,
  "thread_id": "user_3f2a9c...",
  "answer": "## Trip Summary ...",
  "flight_results": "Live flights from DAC to DXB ...",
  "hotel_results": "1. **Hotel name** ...",
  "itinerary": "Day 1 ...",
  "llm_calls": 4
}
```

**Errors** return `{"success": false, "error": "..."}` with status `400` for an empty message or `500` for an internal failure.

### `GET /health`

Returns `{"status": "ok", "message": "AI Travel Planner API is running"}`. Useful for uptime checks and deployment health probes.

## ⚠️ Limitations

- **No ticket prices.** AviationStack provides live and scheduled flight status, not fares. The generated budget is an estimate. For real fares, integrate a pricing API such as Amadeus.
- **Hotels come from web search.** Results are search snippets and links, not live availability or booking inventory.
- **Rule-based route detection.** Unusual phrasing may fall back to the default origin or return broader flight results.
- **API quotas apply.** Free tiers of Groq, Tavily and AviationStack have rate and usage limits.
- **Always verify details** such as visas, prices and schedules with official sources before booking.

## 🗺️ Roadmap

- [ ] Integrate a flight-pricing API for real fares
- [ ] Add hotel availability and price data
- [ ] Stream the plan to the UI as each agent finishes
- [ ] Add user accounts and a saved-trips history
- [ ] Add automated tests and a CI workflow
- [ ] Provide a `Dockerfile` for one-command deployment

## 🤝 Contributing

Contributions, issues and feature requests are welcome.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a pull request

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.

## 👤 Author

**Pratik Vishwas Salunkhe**
GitHub: [@Pratik5767](https://github.com/Pratik5767)

<div align="center">

If you find this project useful, consider giving it a ⭐

</div>
