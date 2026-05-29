# Polyglot - Multilingual Translator on a Custom Agent Framework

A Duolingo-style translator web app, built on a **custom-from-scratch** agent framework. Translates between Indian languages (Hindi, Telugu, Marathi, Gujarati, Bhojpuri, Kannada, Nepali) and Western languages (English, German, French).

## What's inside

- [framework/](framework/) - reusable agent framework (BaseAgent, Pipeline, LLM providers, tool registry). ~250 LOC.
- [agents/](agents/) - concrete agents for this app: detector, router, translator, quality reviewer.
- [backend/](backend/) - FastAPI service exposing `/api/translate` and `/api/languages`.
- [frontend/](frontend/) - React + Vite + Tailwind UI.
- [config/routing.yaml](config/routing.yaml) - language-pair -> LLM routing rules.
- [tests/](tests/) - unit tests (pytest).

## Architecture

```
React (Vite + Tailwind) -> FastAPI -> TranslationPipeline:
  LanguageDetectorAgent -> RouterAgent -> TranslatorAgent -> QualityReviewerAgent
                                              |
                                              v
                         LLM Providers: Claude / OpenAI / IndicTrans2
```

The pipeline retries with a stronger provider when the reviewer scores below 3/5.

## Setup

### Backend

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Optional: enable IndicTrans2 for Bhojpuri / Nepali (downloads ~2GB on first run)
# pip install -r requirements-indictrans.txt
# Then set ENABLE_INDICTRANS2=1 in .env

copy .env.example .env
# Fill in ANTHROPIC_API_KEY and OPENAI_API_KEY

uvicorn backend.main:app --reload
```

Backend runs on http://localhost:8000. Try:
```powershell
curl -X POST http://localhost:8000/api/translate `
  -H "Content-Type: application/json" `
  -d '{"source_lang":"hi","target_lang":"en","text":"नमस्ते, आप कैसे हैं?"}'
```

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. The Vite dev server proxies `/api/*` to the backend.

## Tests

```powershell
pytest
```

Tests use fake LLM providers - no API keys needed.

## How the custom framework works

1. **`Context`** ([framework/context.py](framework/context.py)) flows between agents. Each agent reads and mutates it.
2. **`BaseAgent`** ([framework/agent.py](framework/agent.py)) is the abstract base. Subclasses implement `run(ctx) -> ctx`. The `__call__` wrapper times the agent and catches exceptions into `ctx.errors`.
3. **`Pipeline`** ([framework/orchestrator.py](framework/orchestrator.py)) runs agents in order, short-circuits on errors, supports a `stop_when` predicate.
4. **`LLMProvider`** ([framework/llm.py](framework/llm.py)) is a Protocol. `ClaudeProvider`, `OpenAIProvider`, and `IndicTrans2Provider` adapt different SDKs to a uniform `.complete()` API.
5. **`@tool`** ([framework/tools.py](framework/tools.py)) registers helper functions in a global registry - extensibility hook for future agents (quizzes, lessons).

For the translator specifically, [agents/pipeline.py](agents/pipeline.py) implements a custom retry loop on top of the framework primitives (since the standard `Pipeline` is linear; retries need a small bespoke loop).

## Adding a new language pair

Edit [config/routing.yaml](config/routing.yaml). No code changes needed if an existing provider supports it.

## What's NOT here (v2 scope)

- Audio / TTS / pronunciation
- Quizzes, lessons, streaks, user accounts
- Caching layer (Redis)
- Streaming responses
Deployment test - Thu, May 28, 2026 10:36:17 PM
