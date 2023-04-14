
from sqlalchemy import Integer, Column, String, Numeric

from shared.database import Base


class Game(Base):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(80), nullable=False)
    descricao = Column(String(255))
    imagem = Column(String())
    genero = Column(String(50))
    desenvolvedor = Column(String(50))
    plataforma = Column(String(50))
    valor = Column(Numeric)
