from fastapi import FastAPI
from .db.database import engine
from .db import models
from .api.routes import expenses, users, auth
from fastapi.middleware.cors import CORSMiddleware

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all for now (dev only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(expenses.router)
app.include_router(users.router)
app.include_router(auth.router)