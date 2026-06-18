from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from database.connection import SessionLocal
from controllers.premium_controller import PremiumController
from schemas.user_schema import ActivatePremiumRequest
from utils.jwt_handler import decode_access_token

router = APIRouter()

controller = PremiumController()


def get_username_from_token(authorization: Optional[str]) -> str:
    """Helper: ekstrak username dari header Authorization: Bearer <token>"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Token tidak valid atau expired"
        )

    token = authorization.split(" ")[1]
    payload = decode_access_token(token)

    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=401,
            detail="Token tidak valid atau expired"
        )

    return payload["sub"]  # username


@router.get("/user/premium-status")
def get_premium_status(
    user_id: int,
    authorization: Optional[str] = Header(default=None)
):
    requester_username = get_username_from_token(authorization)

    db = SessionLocal()

    try:
        return controller.get_premium_status(db, user_id, requester_username)

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.post("/user/activate-premium")
def activate_premium(
    body: ActivatePremiumRequest,
    authorization: Optional[str] = Header(default=None)
):
    admin_username = get_username_from_token(authorization)

    db = SessionLocal()

    try:
        return controller.activate_premium(db, body.user_id, admin_username)

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()
