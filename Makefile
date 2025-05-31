fast_api_start:
	cd backend/ && . app/.venv/bin/activate && uvicorn app.main:app --reload
frontend_start:
	cd frontend && pnpm run dev