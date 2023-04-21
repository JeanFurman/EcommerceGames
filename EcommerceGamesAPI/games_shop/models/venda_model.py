from sqlalchemy import Integer, Column, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from shared.database import Base


class Venda(Base):
    __tablename__ = 'vendas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    usuario = relationship('Usuario')
    criado_em = Column(DateTime, default=datetime.now())
    valor_total = Column(Numeric)
