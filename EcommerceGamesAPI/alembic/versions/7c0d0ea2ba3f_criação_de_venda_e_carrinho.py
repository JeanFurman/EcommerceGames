"""Criação de venda e carrinho

Revision ID: 7c0d0ea2ba3f
Revises: d1ef9c68d627
Create Date: 2023-04-19 15:43:31.979263

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c0d0ea2ba3f'
down_revision = 'd1ef9c68d627'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('games',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.String(length=80), nullable=False),
    sa.Column('descricao', sa.String(length=255), nullable=True),
    sa.Column('imagem', sa.String(), nullable=True),
    sa.Column('genero', sa.String(length=50), nullable=True),
    sa.Column('desenvolvedor', sa.String(length=50), nullable=True),
    sa.Column('plataforma', sa.String(length=50), nullable=True),
    sa.Column('valor', sa.Numeric(), nullable=True),
    sa.Column('quantidade', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usuarios',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.String(length=80), nullable=False),
    sa.Column('senha', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('vendas',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=True),
    sa.Column('criado_em', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('carrinhos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('quantidade', sa.Integer(), nullable=True),
    sa.Column('game_id', sa.Integer(), nullable=True),
    sa.Column('vendas_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
    sa.ForeignKeyConstraint(['vendas_id'], ['vendas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('usuario')
    op.drop_table('game')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.Column('descricao', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('genero', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('desenvolvedor', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('plataforma', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('valor', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('imagem', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('quantidade', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='game_pkey')
    )
    op.create_table('usuario',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.Column('senha', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='usuario_pkey'),
    sa.UniqueConstraint('email', name='usuario_email_key')
    )
    op.drop_table('carrinhos')
    op.drop_table('vendas')
    op.drop_table('usuarios')
    op.drop_table('games')
    # ### end Alembic commands ###
