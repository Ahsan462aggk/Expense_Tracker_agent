# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.database import create_db_and_tables
from app.routers.expense_router import router as expense_router
from app.routers.agent_router import router as agent_router
from app.routers.user_router import router as user_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    lifespan=lifespan,
    title="Expense Tracker Application",
    version="1.0.0",
)

# CORS Configuration
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    # Add other allowed origins here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Allow cookies to be sent
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_router)
app.include_router(expense_router)
app.include_router(agent_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Expense Tracker Application"}
