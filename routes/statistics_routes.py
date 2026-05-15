from fastapi import APIRouter
from database.connection import SessionLocal
from controllers.statistics_controller import StatisticsController

router = APIRouter()

controller = StatisticsController()


@router.get("/statistics/{user_id}")
def get_statistics(user_id: int):

    db = SessionLocal()

    try:
        return controller.get_statistics(
            db,
            user_id
        )

    finally:
        db.close()