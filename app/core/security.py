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

def get_current_financeiro(db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Acesso restrito ao Tesoureiro",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        cpf: str = payload.get("sub")
        cargos = payload.get("cargos", [])
        # Tesoureiro, Segundo_Tesoureiro, primeiro_usuario, Pastor
        if cpf is None or ("Tesoureiro" not in cargos and "Segundo_Tesoureiro" not in cargos and "primeiro_usuario" not in cargos and "Pastor" not in cargos):
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.Usuario).filter(models.Usuario.cpf == cpf).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_lideranca(db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Acesso restrito a Liderança",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        cpf: str = payload.get("sub")
        cargos = payload.get("cargos", [])
        # Secretario, Segundo_Secretario, Tesoureiro, Segundo_Tesoureiro, Pastor, Diacono, Presbitero, Diretor_Patrimonio, primeiro_usuario
        if cpf is None or ("Secretario" not in cargos and "Segundo_Secretario" not in cargos and "Tesoureiro" not in cargos and "Segundo_Tesoureiro" not in cargos and "Pastor" not in cargos and "Diacono" not in cargos and "Presbitero" not in cargos and "Diretor_Patrimonio" not in cargos and "primeiro_usuario" not in cargos):
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.Usuario).filter(models.Usuario.cpf == cpf).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_secretario(db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Acesso restrito ao Secretario",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        cpf: str = payload.get("sub")
        cargos = payload.get("cargos", [])
        if cpf is None or ("Secretario" not in cargos and "Segundo_Secretario" not in cargos and "primeiro_usuario" not in cargos and "Pastor" not in cargos):
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.Usuario).filter(models.Usuario.cpf == cpf).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_diretor_patrimonio(db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Acesso restrito ao Diretor de Patrimônio",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        cpf: str = payload.get("sub")
        cargos = payload.get("cargos", [])
        if cpf is None or ("Diretor_Patrimonio" not in cargos and "primeiro_usuario" not in cargos and "Pastor" not in cargos):
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.Usuario).filter(models.Usuario.cpf == cpf).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_diacono(db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Acesso restrito ao Diácono",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        cpf: str = payload.get("sub")
        cargos = payload.get("cargos", [])
        if cpf is None or ("Diácono" not in cargos and "primeiro_usuario" not in cargos and "Pastor" not in cargos):
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.Usuario).filter(models.Usuario.cpf == cpf).first()
    if user is None:
        raise credentials_exception
    return user