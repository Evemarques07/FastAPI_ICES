from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.core.security import get_current_secretario, verify_password, get_password_hash

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.get("/listar", response_model=list[schemas.usuario.UsuarioOut])
def listar_usuarios(db: Session = Depends(database.get_db), user=Depends(get_current_secretario)):
    usuarios = db.query(models.usuario.Usuario).filter(models.usuario.Usuario.membro_id != 1).all()
    # Adiciona o nome do membro ao retorno
    result = []
    for usuario in usuarios:
        usuario_out = schemas.usuario.UsuarioOut.model_validate(usuario, from_attributes=True)
        membro = db.query(models.membro.Membro).filter_by(id=usuario.membro_id).first()
        usuario_out.nome = membro.nome if membro else None
        result.append(usuario_out)
    return result

@router.post("/", response_model=schemas.usuario.UsuarioOut)
def criar_usuario(membro_id: int, db: Session = Depends(database.get_db), user=Depends(get_current_secretario)):
    membro = db.query(models.membro.Membro).filter_by(id=membro_id).first()
    if not membro or not membro.cpf:
        raise HTTPException(status_code=400, detail="Membro não encontrado ou sem CPF")
    if db.query(models.usuario.Usuario).filter_by(cpf=membro.cpf).first():
        raise HTTPException(status_code=400, detail="Usuário já existe para este CPF")
    usuario = models.usuario.Usuario(
        membro_id=membro_id,
        cpf=membro.cpf,
        senha_hash=get_password_hash("1234")
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.put("/senha")
def editar_senha(nova_senha: str, db: Session = Depends(database.get_db), user=Depends(get_current_secretario)):
    usuario = db.query(models.usuario.Usuario).filter_by(id=user.id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    usuario.senha_hash = get_password_hash(nova_senha)
    db.commit()
    return {"message": "Senha alterada com sucesso"}

@router.delete("/{usuario_id}")
def deletar_usuario(usuario_id: int, db: Session = Depends(database.get_db), user=Depends(get_current_secretario)):
    usuario = db.query(models.usuario.Usuario).filter_by(id=usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    db.delete(usuario)
    db.commit()
    return {"message": "Usuário deletado com sucesso"}
