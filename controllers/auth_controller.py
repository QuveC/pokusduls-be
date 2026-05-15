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
            raise Exception("Username already exists")

        new_user = User(
            username=user.username,
            email=user.email,
            password_hash=hash_password(user.password)
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "Register success",
            "user_id": new_user.user_id
        }

    def login(self, db, user):

        found = db.query(User).filter(
            User.username == user.username
        ).first()

        if not found:
            raise Exception("User not found")

        valid = verify_password(
            user.password,
            found.password_hash
        )

        if not valid:
            raise Exception("Wrong password")

        token = create_access_token(
            {"sub": found.username}
        )

        return {
            "token": token,
            "user_id": found.user_id
        }