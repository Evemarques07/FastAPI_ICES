from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, database
from app.core.security import get_current_user

router = APIRouter(prefix="/cargos", tags=["cargos"])

@router.post("/", response_model=schemas.cargo.CargoOut)
def create_cargo(cargo: schemas.cargo.CargoCreate, db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    db_cargo = models.cargo.Cargo(**cargo.dict())
    db.add(db_cargo)
    db.commit()
    db.refresh(db_cargo)
    return db_cargo


@router.get("/", response_model=List[schemas.cargo.CargoOut])
def list_cargos(db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    return db.query(models.cargo.Cargo).all()

# Endpoint para vincular membro a cargo
@router.post("/vincular", status_code=201)
def vincular_membro_cargo(
    membro_id: int,
    cargo_id: int,
    db: Session = Depends(database.get_db),
    user=Depends(get_current_user)
):
    membro = db.query(models.membro.Membro).filter_by(id=membro_id).first()
    cargo = db.query(models.cargo.Cargo).filter_by(id=cargo_id).first()
    if not membro or not cargo:
        raise HTTPException(status_code=404, detail="Membro ou Cargo não encontrado")
    # Verifica se já existe vínculo
    if db.query(models.cargo.CargoMembro).filter_by(membro_id=membro_id, cargo_id=cargo_id).first():
        raise HTTPException(status_code=400, detail="Vínculo já existe")
    vinculo = models.cargo.CargoMembro(membro_id=membro_id, cargo_id=cargo_id)
    db.add(vinculo)
    db.commit()
    db.refresh(vinculo)
    return {"message": "Membro vinculado ao cargo com sucesso!"}

# Desvincular membro de cargo
@router.delete("/desvincular", status_code=200)
def desvincular_membro_cargo(
    membro_id: int,
    cargo_id: int,
    db: Session = Depends(database.get_db),
    user=Depends(get_current_user)
):
    vinculo = db.query(models.cargo.CargoMembro).filter_by(membro_id=membro_id, cargo_id=cargo_id).first()
    if not vinculo:
        raise HTTPException(status_code=404, detail="Vínculo não encontrado")
    db.delete(vinculo)
    db.commit()
    return {"message": "Membro desvinculado do cargo com sucesso!"}


@router.get("/membro/{membro_id}", response_model=List[schemas.cargo.CargoOut])
def list_cargos_por_membro(membro_id: int, db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    return db.query(models.cargo.Cargo) \
        .join(models.cargo.CargoMembro, models.cargo.Cargo.id == models.cargo.CargoMembro.cargo_id) \
        .filter(models.cargo.CargoMembro.membro_id == membro_id) \
        .all()

@router.get("/membros", response_model=List[dict])
def list_membros_com_cargos(db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    vinculos = db.query(models.cargo.CargoMembro).all()
    membros_com_cargos = []
    for vinculo in vinculos:
        membro = db.query(models.membro.Membro).filter_by(id=vinculo.membro_id).first()
        cargo = db.query(models.cargo.Cargo).filter_by(id=vinculo.cargo_id).first()
        if membro and cargo:
            membros_com_cargos.append({
                "membro": {
                    "id": membro.id,
                    "nome": membro.nome,
                    "cpf": membro.cpf,
                    "email": membro.email,
                },
                "cargo": schemas.cargo.CargoOut.from_orm(cargo)
            })
    return membros_com_cargos