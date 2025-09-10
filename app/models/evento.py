from sqlalchemy import Column, Integer, String, Date, Boolean
from app.database import Base

class Evento(Base):
    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    descricao = Column(String(500), nullable=True)
    data_inicio = Column(Date, nullable=False)
    data_final = Column(Date, nullable=False)
    ativo = Column(Boolean, default=True)
