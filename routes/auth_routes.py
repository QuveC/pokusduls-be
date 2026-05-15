from fastapi import APIRouter
from database.connection import SessionLocal
from controllers.auth_controller import AuthController
from schemas.user_schema import (
    UserRegister,
    UserLogin
)

router = APIRouter()

controller = AuthController()


@router.post("/register")
def register(user: UserRegister):

    db = SessionLocal()

    try:
        return controller.register(db, user)

    finally:
        db.close()


@router.post("/login")
def login(user: UserLogin):

    db = SessionLocal()

    try:
        return controller.login(db, user)

    finally:
        db.close()