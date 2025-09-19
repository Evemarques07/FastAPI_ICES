from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base

class Patrimonio(Base):
    __tablename__ = 'patrimonios'
    id = Column(Integer, primary_key=True, index=True)
    nome_item = Column(String(50), nullable=False)
    tipo = Column(String(50), nullable=False)
    preco_aquisicao = Column(Float, nullable=False)
    data_aquisicao = Column(Date, nullable=False)
    observacoes = Column(String(255), nullable=True)
