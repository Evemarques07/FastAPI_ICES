from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, database
from app.core.security import get_current_diretor_patrimonio
from fastapi import Query

router = APIRouter(prefix="/patrimonio", tags=["patrimonio"])

@router.post("/", response_model=schemas.patrimonio.PatrimonioOut)
def criar_patrimonio(patrimonio: schemas.patrimonio.PatrimonioCreate, db: Session = Depends(database.get_db), user=Depends(get_current_diretor_patrimonio)):
    db_patrimonio = models.patrimonio.Patrimonio(**patrimonio.dict())
    db.add(db_patrimonio)
    db.commit()
    db.refresh(db_patrimonio)
    return db_patrimonio

@router.get("/", response_model=List[schemas.patrimonio.PatrimonioOut])
def listar_patrimonios(skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=50), db: Session = Depends(database.get_db), user=Depends(get_current_diretor_patrimonio)):
    patrimonios = db.query(models.patrimonio.Patrimonio).offset(skip).limit(limit).all()
    return patrimonios

@router.get("/buscar", response_model=List[schemas.patrimonio.PatrimonioOut])
def buscar_patrimonio_nome(nome_item: str, db: Session = Depends(database.get_db), user=Depends(get_current_diretor_patrimonio)):
    patrimonios = db.query(models.patrimonio.Patrimonio).filter(models.patrimonio.Patrimonio.nome_item.ilike(f"%{nome_item}%")).all()
    return patrimonios

@router.get("/{patrimonio_id}", response_model=schemas.patrimonio.PatrimonioOut)
def buscar_patrimonio_id(patrimonio_id: int, db: Session = Depends(database.get_db), user=Depends(get_current_diretor_patrimonio)):
    patrimonio = db.query(models.patrimonio.Patrimonio).filter_by(id=patrimonio_id).first()
    if not patrimonio:
        raise HTTPException(status_code=404, detail="Patrimônio não encontrado")
    return patrimonio

@router.patch("/{patrimonio_id}", response_model=schemas.patrimonio.PatrimonioOut)
def editar_patrimonio(patrimonio_id: int, patrimonio: schemas.patrimonio.PatrimonioUpdate, db: Session = Depends(database.get_db), user=Depends(get_current_diretor_patrimonio)):
    db_patrimonio = db.query(models.patrimonio.Patrimonio).filter_by(id=patrimonio_id).first()
    if not db_patrimonio:
        raise HTTPException(status_code=404, detail="Patrimônio não encontrado")
    for key, value in patrimonio.dict(exclude_unset=True).items():
        setattr(db_patrimonio, key, value)
    db.commit()
    db.refresh(db_patrimonio)
    return db_patrimonio

@router.delete("/{patrimonio_id}", response_model=dict)
def deletar_patrimonio(patrimonio_id: int, db: Session = Depends(database.get_db), user=Depends(get_current_diretor_patrimonio)):
    db_patrimonio = db.query(models.patrimonio.Patrimonio).filter_by(id=patrimonio_id).first()
    if not db_patrimonio:
        raise HTTPException(status_code=404, detail="Patrimônio não encontrado")
    db.delete(db_patrimonio)
    db.commit()
    return {"message": "Patrimônio deletado com sucesso"}
