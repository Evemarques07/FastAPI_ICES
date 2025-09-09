from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base

class SaidaMissionaria(Base):
    __tablename__ = 'saidas_missionarias'
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(255), nullable=False)
    valor = Column(Float, nullable=False)
    data = Column(Date, nullable=False)
    descricao = Column(String(255), nullable=True)
