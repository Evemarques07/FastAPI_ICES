from dotenv import load_dotenv
load_dotenv()
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv('DATABASE_URL')


try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        print(f"Conexão com o banco realizada com sucesso: {conn}")
except Exception as e:
    print(f"Erro ao conectar no banco: {e}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
