import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.auth_routes import router as auth_router
from app.api.v1.interactions_routes import router as interactions_router
from app.api.v1.recommender_routes import recommender_router
from app.api.v1.similar_user import router as similar_user_router
from app.api.v1.statistic_routes import router as statistic_router
from app.api.v1.user_routes import router as user_router

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:5173",
]

# Подключение CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router=user_router)
app.include_router(router=auth_router)
app.include_router(recommender_router, prefix="/recommender", tags=["Recommender System"])
app.include_router(router=statistic_router)
app.include_router(router=similar_user_router)
app.include_router(router=interactions_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
