"""initial

"""
revision = '20230903_ices_initial'
down_revision = None
branch_labels = None
depends_on = None
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table('membros',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('nome', sa.String(255), nullable=False),
        sa.Column('data_nascimento', sa.Date(), nullable=False),
        sa.Column('telefone', sa.String(255), nullable=True),
        sa.Column('email', sa.String(255), nullable=True),
        sa.Column('endereco', sa.String(255), nullable=True),
        sa.Column('data_entrada', sa.Date(), nullable=False),
        sa.Column('ativo', sa.Boolean(), default=True),
        sa.Column('cpf', sa.String(255), unique=True, nullable=True),
        sa.Column('foto', sa.LargeBinary(), nullable=True)
    )
    op.create_table('usuarios',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('cpf', sa.String(255), unique=True, nullable=False, index=True),
        sa.Column('senha_hash', sa.String(255), nullable=False),
        sa.Column('ativo', sa.Boolean(), default=True),
        sa.Column('membro_id', sa.Integer(), sa.ForeignKey('membros.id'), nullable=False)
    )
    op.create_table('cargos',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('nome', sa.String(255), unique=True, nullable=False)
    )
    op.create_table('cargos_membros',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('membro_id', sa.Integer(), sa.ForeignKey('membros.id'), nullable=False),
        sa.Column('cargo_id', sa.Integer(), sa.ForeignKey('cargos.id'), nullable=False)
    )
    op.create_table('entradas_financeiras',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('tipo', sa.String(255), nullable=False),
        sa.Column('valor', sa.Float(), nullable=False),
        sa.Column('data', sa.Date(), nullable=False),
        sa.Column('descricao', sa.String(255), nullable=True),
        sa.Column('membro_id', sa.Integer(), sa.ForeignKey('membros.id'), nullable=True)
    )
    op.create_table('saidas_financeiras',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('tipo', sa.String(255), nullable=False),
        sa.Column('valor', sa.Float(), nullable=False),
        sa.Column('data', sa.Date(), nullable=False),
        sa.Column('descricao', sa.String(255), nullable=True)
    )

def downgrade():
    op.drop_table('saidas_financeiras')
    op.drop_table('entradas_financeiras')
    op.drop_table('cargos_membros')
    op.drop_table('cargos')
    op.drop_table('usuarios')
    op.drop_table('membros')
