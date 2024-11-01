import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.v1.router import router as v1_router
from config.config import app_settings
from models.user import User
from database.database import SessionLocal, engine

def create_app() -> FastAPI:
    app = FastAPI(title="Payroll Application")
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include version 1 router
    app.include_router(v1_router)
    
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=app_settings.SERVICE_PORT, reload=True)
