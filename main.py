import uvicorn
from fastapi import FastAPI
from src.api.router import router as api_router

app = FastAPI()

# Включаємо головний роутер з префіксом /api
app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    # uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
