from fastapi import HTTPException
from datetime import datetime
from models.user import User


class PremiumController:

    def get_premium_status(self, db, user_id: int, requester_username: str):
        """
        Cek status premium user.
        requester_username diambil dari JWT — validasi bahwa
        user hanya bisa cek miliknya sendiri (kecuali admin).
        """
        user = db.query(User).filter(User.user_id == user_id).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User tidak ditemukan"
            )

        # Pastikan token milik user yang sama (atau admin)
        if user.username != requester_username:
            raise HTTPException(
                status_code=403,
                detail="Tidak diizinkan mengakses data user lain"
            )

        return {
            "is_premium": bool(user.is_premium),
            "premium_activated_at": user.premium_activated_at
        }

    def activate_premium(self, db, user_id: int, admin_username: str):
        """
        Aktifkan premium untuk user tertentu.
        Hanya dipanggil oleh admin.
        """
        user = db.query(User).filter(User.user_id == user_id).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User tidak ditemukan"
            )

        if user.is_premium:
            raise HTTPException(
                status_code=400,
                detail="User sudah premium"
            )

        user.is_premium = True
        user.premium_activated_at = datetime.utcnow()
        user.premium_activated_by = admin_username

        db.commit()
        db.refresh(user)

        return {
            "message": "Premium berhasil diaktifkan",
            "user_id": user.user_id,
            "is_premium": bool(user.is_premium),
            "activated_at": user.premium_activated_at
        }
