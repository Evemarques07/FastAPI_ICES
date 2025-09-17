from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, membros, cargos, entradas, saidas, relatorios, usuarios, filtros, eventos, escalas, filhos

app = FastAPI()

app.include_router(auth.router)
app.include_router(membros.router)
app.include_router(cargos.router)
app.include_router(entradas.router)
app.include_router(saidas.router)
app.include_router(relatorios.router)
app.include_router(usuarios.router)
app.include_router(filtros.router)
app.include_router(eventos.router)
app.include_router(escalas.router)
app.include_router(filhos.router)

app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://localhost:5173", "https://icesiqueiraapp.web.app"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)

