from sqlalchemy import func
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, database
from app.core.security import get_current_user

router = APIRouter(prefix="/saidas", tags=["saidas"])

@router.post("/", response_model=schemas.saida_financeira.SaidaFinanceiraOut)
def create_saida(saida: schemas.saida_financeira.SaidaFinanceiraCreate, db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    db_saida = models.saida_financeira.SaidaFinanceira(**saida.dict())
    db.add(db_saida)
    db.commit()
    db.refresh(db_saida)
    return db_saida

@router.get("/", response_model=List[schemas.saida_financeira.SaidaFinanceiraOut])
def list_saidas(
    user=Depends(get_current_user),
    db: Session = Depends(database.get_db),
    skip: int = 0,
    limit: int = 10
):
    return db.query(models.saida_financeira.SaidaFinanceira) \
        .order_by(models.saida_financeira.SaidaFinanceira.data.desc()) \
        .offset(skip).limit(limit).all()

# Atualizar saída financeira
@router.put("/financeiro/{saida_id}", response_model=schemas.saida_financeira.SaidaFinanceiraOut)
def update_saida_financeira(saida_id: int, saida: schemas.saida_financeira.SaidaFinanceiraCreate, db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    db_saida = db.query(models.saida_financeira.SaidaFinanceira).filter_by(id=saida_id).first()
    if not db_saida:
        raise HTTPException(status_code=404, detail="Saída financeira não encontrada")
    for key, value in saida.dict().items():
        setattr(db_saida, key, value)
    db.commit()
    db.refresh(db_saida)
    return db_saida

# Atualizar saída missionária
@router.put("/missoes/{saida_id}", response_model=dict)
def update_saida_missionaria(saida_id: int, saida: dict, db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    db_saida = db.query(models.saida_missionaria.SaidaMissionaria).filter_by(id=saida_id).first()
    if not db_saida:
        raise HTTPException(status_code=404, detail="Saída missionária não encontrada")
    for key, value in saida.items():
        setattr(db_saida, key, value)
    db.commit()
    db.refresh(db_saida)
    return db_saida.__dict__

# Atualizar saída de projetos
@router.put("/projetos/{saida_id}", response_model=dict)
def update_saida_projetos(saida_id: int, saida: dict, db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    db_saida = db.query(models.saida_projetos.SaidaProjetos).filter_by(id=saida_id).first()
    if not db_saida:
        raise HTTPException(status_code=404, detail="Saída de projetos não encontrada")
    for key, value in saida.items():
        setattr(db_saida, key, value)
    db.commit()
    db.refresh(db_saida)
    return db_saida.__dict__

# Deletar saída financeira
@router.delete("/financeiro/{saida_id}", response_model=dict)
def delete_saida_financeira(saida_id: int, db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    db_saida = db.query(models.saida_financeira.SaidaFinanceira).filter_by(id=saida_id).first()
    if not db_saida:
        raise HTTPException(status_code=404, detail="Saída financeira não encontrada")
    db.delete(db_saida)
    db.commit()
    return {"message": "Saída financeira deletada com sucesso"}

# Deletar saída missionária
@router.delete("/missoes/{saida_id}", response_model=dict)
def delete_saida_missionaria(saida_id: int, db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    db_saida = db.query(models.saida_missionaria.SaidaMissionaria).filter_by(id=saida_id).first()
    if not db_saida:
        raise HTTPException(status_code=404, detail="Saída missionária não encontrada")
    db.delete(db_saida)
    db.commit()
    return {"message": "Saída missionária deletada com sucesso"}

# Deletar saída de projetos
@router.delete("/projetos/{saida_id}", response_model=dict)
def delete_saida_projetos(saida_id: int, db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    db_saida = db.query(models.saida_projetos.SaidaProjetos).filter_by(id=saida_id).first()
    if not db_saida:
        raise HTTPException(status_code=404, detail="Saída de projetos não encontrada")
    db.delete(db_saida)
    db.commit()
    return {"message": "Saída de projetos deletada com sucesso"}

@router.get("/missoes", response_model=List[dict])
def list_saidas_missoes(
    user=Depends(get_current_user),
    db: Session = Depends(database.get_db),
    skip: int = 0,
    limit: int = 10
):
    query = db.query(models.saida_missionaria.SaidaMissionaria) \
        .order_by(models.saida_missionaria.SaidaMissionaria.data.desc()) \
        .offset(skip).limit(limit)
    result = []
    for saida in query:
        saida_dict = saida.__dict__.copy()
        saida_dict.pop('_sa_instance_state', None)
        result.append(saida_dict)
    return result

@router.get("/projetos", response_model=List[dict])
def list_saidas_projetos(
    user=Depends(get_current_user),
    db: Session = Depends(database.get_db),
    skip: int = 0,
    limit: int = 10
):
    query = db.query(models.saida_projetos.SaidaProjetos) \
        .order_by(models.saida_projetos.SaidaProjetos.data.desc()) \
        .offset(skip).limit(limit)
    result = []
    for saida in query:
        saida_dict = saida.__dict__.copy()
        saida_dict.pop('_sa_instance_state', None)
        result.append(saida_dict)
    return result

@router.get("/soma", response_model=dict)
def soma_saidas(
    tipo: str = None,  # 'financeira', 'missionaria', 'projetos' ou None para todas
    data_inicio: str = None,
    data_fim: str = None,
    user=Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    filtros = []
    if data_inicio:
        filtros.append(lambda col: col.data >= data_inicio)
    if data_fim:
        filtros.append(lambda col: col.data <= data_fim)

    def soma_model(model):
        query = db.query(func.sum(model.valor))
        for f in filtros:
            query = query.filter(f(model))
        return query.scalar() or 0

    resultado = {}
    if not tipo or tipo == 'financeira':
        resultado['soma_financeiras'] = soma_model(models.saida_financeira.SaidaFinanceira)
    if not tipo or tipo == 'missionaria':
        resultado['soma_missoes'] = soma_model(models.saida_missionaria.SaidaMissionaria)
    if not tipo or tipo == 'projetos':
        resultado['soma_projetos'] = soma_model(models.saida_projetos.SaidaProjetos)
    return resultado