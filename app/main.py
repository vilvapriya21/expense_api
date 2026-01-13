from fastapi import FastAPI
from .db.database import engine
from .db import models
from .api.routes import expenses, users, auth

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API")

# Include routers
app.include_router(expenses.router)
app.include_router(users.router)
app.include_router(auth.router)