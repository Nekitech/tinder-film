fast_api_start:
	cd backend/ && . app/.venv/bin/activate && uvicorn app.main:app --reload
frontend_start:
	cd frontend && pnpm run dev

generate_scheme:
	cd frontend && npx openapi-typescript http://127.0.0.1:8000/openapi.json -o src/shared/api/generated/schema.d.ts

generate_migration:
	 alembic revision --autogenerate -m ""
