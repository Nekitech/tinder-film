import uvicorn
from fastapi import FastAPI

from app.api.v1.auth_routes import router as auth_router
from app.api.v1.user_routes import router as user_router

app = FastAPI()

app.include_router(router=user_router)
app.include_router(router=auth_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
