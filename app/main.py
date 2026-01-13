from fastapi import FastAPI
from app.routes import router as leave_router

app = FastAPI(title="Employee Leave API")

app.include_router(leave_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}