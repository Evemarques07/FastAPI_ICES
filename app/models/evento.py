from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime
from app.database import Base

class Evento(Base):
    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    descricao = Column(String(500), nullable=True)
    data_inicio = Column(DateTime, nullable=False)
    data_final = Column(DateTime, nullable=False)
    ativo = Column(Boolean, default=True)
