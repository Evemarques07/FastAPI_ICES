from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app import models, database
import os

SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        cpf: str = payload.get("sub")
        if cpf is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.Usuario).filter(models.Usuario.cpf == cpf).first()
    if user is None:
        raise credentials_exception
    return user

# def has_cargo(user, cargo_nome):
#     return any(
#         cargo_membro.cargo.nome.lower() == cargo_nome.lower()
#         for cargo_membro in getattr(user, 'cargos', [])
#     )

# def get_pastor(current_user=Depends(get_current_user)):
#     if not has_cargo(current_user, 'Pastor'):
#         raise HTTPException(status_code=403, detail="Acesso restrito a Pastores")
#     return current_user

# def get_secretario(current_user=Depends(get_current_user)):
#     if not has_cargo(current_user, 'Secretario'):
#         raise HTTPException(status_code=403, detail="Acesso restrito a Secretários")
#     return current_user

# def get_segundo_secretario(current_user=Depends(get_current_user)):
#     if not has_cargo(current_user, 'Segundo_Secretario'):
#         raise HTTPException(status_code=403, detail="Acesso restrito a 2º Secretários")
#     return current_user

# def get_tesoureiro(current_user=Depends(get_current_user)):
#     if not has_cargo(current_user, 'Tesoureiro'):
#         raise HTTPException(status_code=403, detail="Acesso restrito a Tesoureiros")
#     return current_user

# def get_segundo_tesoureiro(current_user=Depends(get_current_user)):
#     if not has_cargo(current_user, 'Segundo_Tesoureiro'):
#         raise HTTPException(status_code=403, detail="Acesso restrito a 2º Tesoureiros")
#     return current_user

# def get_diretor_patrimonio(current_user=Depends(get_current_user)):
#     if not has_cargo(current_user, 'Diretor_Patrimonio'):
#         raise HTTPException(status_code=403, detail="Acesso restrito a Diretor de Patrimônio")
#     return current_user

# def get_diacono(current_user=Depends(get_current_user)):
#     if not has_cargo(current_user, 'Diacono'):
#         raise HTTPException(status_code=403, detail="Acesso restrito a Diáconos")
#     return current_user

# def get_presbitero(current_user=Depends(get_current_user)):
#     if not has_cargo(current_user, 'Presbitero'):
#         raise HTTPException(status_code=403, detail="Acesso restrito a Presbíteros")
#     return current_user

# def get_primeiro_usuario(current_user=Depends(get_current_user)):
#     if not has_cargo(current_user, 'primeiro_usuario'):
#         raise HTTPException(status_code=403, detail="Acesso restrito ao usuário master")
#     return current_user