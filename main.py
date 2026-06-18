from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel

from database.connection import Base, engine
from models.user import User

app = FastAPI()

# ROUTES
from routes import (
    auth_routes,
    session_routes,
    monitoring_routes,
    statistics_routes,
    chat_routes,
    premium_routes
)

# EXCEPTION HANDLER
from utils.exception_handler import (
    validation_exception_handler,
    sqlalchemy_exception_handler,
    http_exception_handler
)

# =====================================
# FASTAPI APP
# =====================================

app = FastAPI(
    title="PokusDuls API",
    description="Backend API for Smart Study Assistant",
    version="1.0.0"
)

# =====================================
# CORS
# =====================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================
# DATABASE CREATE TABLE
# =====================================

Base.metadata.create_all(bind=engine)

# =====================================
# GLOBAL EXCEPTION HANDLER
# =====================================

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.add_exception_handler(
    SQLAlchemyError,
    sqlalchemy_exception_handler
)

app.add_exception_handler(
    HTTPException,
    http_exception_handler
)

# =====================================
# INCLUDE ROUTES
# =====================================

app.include_router(
    auth_routes.router,
    tags=["Authentication"]
)

app.include_router(
    session_routes.router,
    tags=["Session"]
)

app.include_router(
    monitoring_routes.router,
    tags=["Monitoring"]
)

app.include_router(
    statistics_routes.router,
    tags=["Statistics"]
)

app.include_router(
    chat_routes.router,
    tags=["Chatbot"]
)

app.include_router(
    premium_routes.router,
    tags=["Premium"]
)

# =====================================
# ROOT ENDPOINT
# =====================================

@app.get("/")
def root():
    return {
        "success": True,
        "message": "PokusDuls Backend Running 🚀"
    }

# =====================================
# HEALTH CHECK
# =====================================

@app.get("/health")
def health_check():
    return {
        "status": "OK",
        "database": "connected"
    }

# =====================================
# TEST ERROR ENDPOINT
# =====================================

@app.get("/test-error")
def test_error():
    raise HTTPException(
        status_code=400,
        detail="Test Error Handler"
    )
    

