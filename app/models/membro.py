from sqlalchemy import Column, Integer, String, Date, Boolean, LargeBinary, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class Membro(Base):
    __tablename__ = 'membros'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    telefone = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    endereco = Column(String(255), nullable=True)
    data_entrada = Column(Date, nullable=False)
    ativo = Column(Boolean, default=True)
    cpf = Column(String(255), unique=True, nullable=True)
    sexo = Column(String(10), nullable=True)
    nome_pai = Column(String(255), nullable=True)
    nome_mae = Column(String(255), nullable=True)
    estado_civil = Column(String(20), nullable=True)
    data_casamento = Column(Date, nullable=True)
    nome_conjuge = Column(String(255), nullable=True)
    data_nascimento_conjuge = Column(Date, nullable=True)
    data_batismo = Column(Date, nullable=True)
    foto = Column(String(255), nullable=True)
    tipo = Column(String(20), nullable=False, default='membro') 
    usuario = relationship('Usuario', back_populates='membro', uselist=False)
    cargos = relationship('CargoMembro', back_populates='membro')
    entradas = relationship('EntradaFinanceira', back_populates='membro')
    entradas_projetos = relationship('app.models.entrada_projetos.EntradaProjetos', back_populates='membro')
    entradas_missionarias = relationship('app.models.entrada_missionaria.EntradaMissionaria', back_populates='membro')
    escalas = relationship('Escala', back_populates='membro')
