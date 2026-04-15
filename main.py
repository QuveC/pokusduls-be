from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from hashlib import sha256

app = FastAPI()

# =========================
# CORS (WAJIB)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# DATABASE
# =========================
DATABASE_URL = "mysql+pymysql://root:@localhost/drowsiness_study_app"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# =========================
# MODEL (SESUAI MYSQL)
# =========================
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# ❌ JANGAN PAKE (udah bikin manual di MySQL)
# Base.metadata.create_all(bind=engine)

# =========================
# SCHEMA
# =========================
class UserRegister(BaseModel):
    username: str
    email: str   # ✅ TANPA EmailStr biar ga error
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# =========================
# UML BASE (PUNYA LU - TIDAK DIUBAH)
# =========================

# ----- MODEL -----
class SessionData:
    def __init__(self, duration: int, methodType: str, timestamp: datetime):
        self.duration = duration
        self.methodType = methodType
        self.timestamp = timestamp


class UserStatistics:
    def __init__(self, totalXP: int, currentStreak: int):
        self.totalXP = totalXP
        self.currentStreak = currentStreak


# ----- CONTROLLER -----
class SessionController:
    def startFeynmanSession(self):
        pass

    def validateDuration(self):
        pass


class TimerController:
    def startTimer(self):
        pass

    def pauseTimer(self):
        pass

    def stopTimer(self):
        pass


class GamificationEngine:
    def calculateXP(self):
        pass

    def updateStreak(self):
        pass


class DatabaseHandler:
    def saveSession(self):
        pass

    def fetchUserStats(self):
        pass


# ----- VIEW -----
class HomePageUI:
    pass

class FeynmanSessionUI:
    pass

class TimerRunningUI:
    pass

class SessionCompleteDialog:
    pass

class StatisticsUI:
    pass


# =========================
# HELPER
# =========================
def hash_password(password: str):
    return sha256(password.encode()).hexdigest()

# =========================
# ROUTES
# =========================

@app.get("/")
def root():
    return {"message": "API Running 🚀"}


@app.post("/register")
def register(user: UserRegister):
    db = SessionLocal()

    # cek username/email
    existing = db.query(User).filter(
        (User.username == user.username) |
        (User.email == user.email)
    ).first()

    if existing:
        db.close()
        raise HTTPException(status_code=400, detail="Username atau Email sudah dipakai")

    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()

    return {
        "message": "Register berhasil",
        "user_id": new_user.user_id
    }


@app.post("/login")
def login(user: UserLogin):
    db = SessionLocal()

    # ambil user berdasarkan username aja
    found = db.query(User).filter(
        User.username == user.username
    ).first()

    if not found:
        db.close()
        raise HTTPException(status_code=401, detail="Username tidak ditemukan")

    # hash password input
    hashed_input = hash_password(user.password)

    # bandingkan manual
    if hashed_input != found.password_hash:
        db.close()
        raise HTTPException(status_code=401, detail="Password salah")

    db.close()

    return {
        "message": "Login berhasil",
        "user_id": found.user_id
    }