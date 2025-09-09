from app.database import SessionLocal
from app.models import Membro, Usuario
from app.core.security import get_password_hash
from datetime import date

def create_admin():
    db = SessionLocal()
    # Verifica se já existe
    if db.query(Usuario).filter(Usuario.cpf == '12345678910').first():
        print('Usuário admin já existe.')
        return
    membro = Membro(
        nome='Adão',
        data_nascimento=date(1980, 1, 1),
        telefone='(00) 00000-0000',
        email='adao@admin.com',
        endereco='Rua do Éden, 1',
        data_entrada=date.today(),
        ativo=True,
        cpf='12345678910',
        foto=None
    )
    db.add(membro)
    db.commit()
    db.refresh(membro)
    usuario = Usuario(
        cpf='12345678910',
        senha_hash=get_password_hash('admin123'),
        ativo=True,
        membro_id=membro.id
    )
    db.add(usuario)
    db.commit()
    print('Usuário admin criado com sucesso!')

if __name__ == '__main__':
    create_admin()
