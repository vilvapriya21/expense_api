"""
Main entry point for the Expense Tracker API.

This module initializes the FastAPI application,
configures middleware, sets up database tables,
and registers all API routers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db.database import engine
from .db import models
from .api.routes import expenses, users, auth


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI app instance.
    """
    application = FastAPI(title="Expense Tracker API")

    @application.get("/")
    def root():
        return {
            "status": "running",
            "service": "Expense Tracker API",
            "docs": "/docs"
        }

    # Enable CORS for frontend-backend communication
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Development only
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register API routers
    application.include_router(auth.router)
    application.include_router(users.router)
    application.include_router(expenses.router)

    return application


# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize the FastAPI app
app = create_application()