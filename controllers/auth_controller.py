from fastapi import HTTPException
from models.user import User
from utils.security import (
    hash_password,
    verify_password
)
from utils.jwt_handler import create_access_token

class AuthController:

    def register(self, db, user):

        existing = db.query(User).filter(
            User.username == user.username
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Username sudah digunakan"
            )

        new_user = User(
            username=user.username,
            email=user.email,
            password_hash=hash_password(user.password)
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "Registrasi berhasil! Silakan login.",
            "user_id": new_user.user_id
        }

    def login(self, db, user):

        found = db.query(User).filter(
            User.username == user.username
        ).first()

        if not found:
            raise HTTPException(
                status_code=401,
                detail="Username atau password salah"
            )

        valid = verify_password(
            user.password,
            found.password_hash
        )

        if not valid:
            raise HTTPException(
                status_code=401,
                detail="Username atau password salah"
            )

        token = create_access_token(
            {"sub": found.username}
        )

        return {
            "message": "Login berhasil! Selamat datang.",
            "token": token,
            "user_id": found.user_id
        }
