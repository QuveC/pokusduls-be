<<<<<<< HEAD
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#catatan database url saat ini adalah database local ubah url database ke url masing masing atau pakai database yang di deploy ke server
DATABASE_URL = "mysql+pymysql://root:@localhost/drowsiness_study_app" 

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
=======
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#catatan database url saat ini adalah database local ubah url database ke url masing masing atau pakai database yang di deploy ke server
DATABASE_URL = "mysql+pymysql://root:@localhost/drowsiness_study_app" 

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
>>>>>>> 1925e27 (Penambahan YOLO)
