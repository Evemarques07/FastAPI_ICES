from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.core import security
from app import models, database

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.Usuario).filter(models.Usuario.cpf == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.senha_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="CPF ou senha inválidos")
    if not user.ativo:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuário inativo")
    # Buscar cargos do usuário
    cargos = []
    if user.membro and hasattr(user.membro, 'cargos'):
        for cargo_membro in user.membro.cargos:
            if cargo_membro.cargo and hasattr(cargo_membro.cargo, 'nome'):
                cargos.append(cargo_membro.cargo.nome)
    nome_membro = user.membro.nome if user.membro and hasattr(user.membro, 'nome') else None
    membro_id = user.membro.id if user.membro and hasattr(user.membro, 'id') else None
    access_token = security.create_access_token(data={"sub": user.cpf, "cargos": cargos, "nome_membro": nome_membro})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "nome_membro": nome_membro,
        "membro_id": membro_id,
        "cargos": cargos
    }

@router.get("/me")
def me(current_user: models.Usuario = Depends(security.get_current_user)):
    return {"id": current_user.id, "cpf": current_user.cpf, "ativo": current_user.ativo, "membro_id": current_user.membro_id}

