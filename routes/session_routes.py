from fastapi import APIRouter
from database.connection import SessionLocal
from controllers.session_controller import SessionController
from schemas.session_schema import SessionCreate

router = APIRouter()

controller = SessionController()


@router.post("/session/complete")
def complete_session(data: SessionCreate):

    db = SessionLocal()

    try:
        return controller.complete_session(db, data)

    finally:
        db.close()