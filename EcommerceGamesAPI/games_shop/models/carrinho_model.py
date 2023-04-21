from sqlalchemy import Integer, Column, ForeignKey
from sqlalchemy.orm import relationship

from shared.database import Base


class Carrinho(Base):
    __tablename__ = 'carrinhos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    quantidade = Column(Integer)
    game_id = Column(Integer, ForeignKey('games.id'))
    vendas_id = Column(Integer, ForeignKey('vendas.id'))
    game = relationship('Game')
    venda = relationship('Venda')
