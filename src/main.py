import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.v1.router import router as v1_router
from config.config import app_settings
from models.user import User
from utils.csu import create_admin_user
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


@app.on_event("startup")
async def startup_event():
    async with SessionLocal() as db:
        async with engine.begin() as conn:
            await conn.run_sync(User.metadata.create_all)

        admin_user = await db.execute(User.__table__.select().where(User.is_admin == True))
        admin_user = admin_user.scalars().first()

        if not admin_user:
            await create_admin_user(db)
            print("Admin user created.")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=app_settings.SERVICE_PORT, reload=True)
