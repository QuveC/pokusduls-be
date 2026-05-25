<<<<<<< HEAD
from fastapi import APIRouter, HTTPException
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

    except HTTPException:
        raise  # teruskan HTTPException apa adanya ke FastAPI

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.post("/login")
def login(user: UserLogin):

    db = SessionLocal()

    try:
        return controller.login(db, user)

    except HTTPException:
        raise  # teruskan HTTPException apa adanya ke FastAPI

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()
=======
from fastapi import APIRouter, HTTPException
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

    except HTTPException:
        raise  # teruskan HTTPException apa adanya ke FastAPI

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.post("/login")
def login(user: UserLogin):

    db = SessionLocal()

    try:
        return controller.login(db, user)

    except HTTPException:
        raise  # teruskan HTTPException apa adanya ke FastAPI

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()
>>>>>>> 1925e27 (Penambahan YOLO)
