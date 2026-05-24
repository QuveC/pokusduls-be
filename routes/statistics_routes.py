from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.connection import SessionLocal
from controllers.statistics_controller import StatisticsController

router = APIRouter()
controller = StatisticsController()


class UpdateStatsRequest(BaseModel):
    xp_gained: int = 0
    session_completed: bool = True


@router.get("/statistics/{user_id}")
def get_statistics(user_id: int):
    db = SessionLocal()
    try:
        return controller.get_statistics(db, user_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.post("/statistics/{user_id}/update")
def update_statistics(user_id: int, body: UpdateStatsRequest):
    """
    Dipanggil dari Timer.jsx setiap sesi selesai.
    Menambah XP dan memperbarui streak di tabel user_statistics.
    """
    db = SessionLocal()
    try:
        return controller.update_statistics(
            db,
            user_id=user_id,
            xp_gained=body.xp_gained,
            session_completed=body.session_completed,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
