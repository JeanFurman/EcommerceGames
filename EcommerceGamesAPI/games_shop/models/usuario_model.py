from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import relationship

from games_shop.models.venda_model import Venda
from shared.database import Base


class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(80), nullable=False)
    senha = Column(String(), nullable=False)
    email = Column(String(), nullable=False, unique=True)
