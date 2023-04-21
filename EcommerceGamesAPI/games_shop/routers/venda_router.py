from decimal import Decimal
from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from games_shop.models.carrinho_model import Carrinho
from games_shop.models.games_model import Game
from games_shop.models.usuario_model import Usuario
from games_shop.models.venda_model import Venda
from shared.dependencies import get_db
from games_shop.routers.utils import obter_usuario_logado

router = APIRouter(prefix='/vendas')


class GamesResponse(BaseModel):
    id: int
    nome: str
    descricao: str
    genero: str
    desenvolvedor: str
    plataforma: str
    imagem: str | None
    quantidade: int
    valor: Decimal

    class Config:
        orm_mode = True


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str

    class Config:
        orm_mode = True


class CarrinhoRequest(BaseModel):
    game_id: int = Field()
    quantidade: int = Field(gt=0)


class CarrinhoResponse(BaseModel):
    id: int
    quantidade: int
    game_id: int
    vendas_id: int

    class Config:
        orm_mode = True


class CarrinhoSchema(BaseModel):
    quantidade: int
    game: GamesResponse

    class Config:
        orm_mode = True


class VendaRequest(BaseModel):
    carrinhos: List[CarrinhoResponse]


class VendaResponse(BaseModel):
    id: int
    usuario_id: int
    carrinhos: List[CarrinhoSchema]
    valor_total: Decimal
    criado_em: str

    class Config:
        orm_mode = True


@router.post('', status_code=201)
def criar_venda(carrinho_request: List[CarrinhoRequest], usuario: Usuario = Depends(obter_usuario_logado),
                      db: Session = Depends(get_db)):
    soma = 0
    for i in range(0, len(carrinho_request)):
        game = db.query(Game).get(carrinho_request[i].game_id)
        soma += carrinho_request[i].quantidade * game.valor
        if carrinho_request[i].quantidade > game.quantidade:
            raise HTTPException(status_code=400, detail='Quantidade excedida')
    venda = Venda(usuario_id=usuario.id, valor_total=soma)
    db.add(venda)
    db.commit()
    db.refresh(venda)
    carrinhos = []
    games = []
    for i in range(0, len(carrinho_request)):
        game = db.query(Game).get(carrinho_request[i].game_id)
        game.quantidade = game.quantidade - carrinho_request[i].quantidade
        games.append(game)
        carrinhos.append(Carrinho(quantidade=carrinho_request[i].quantidade,
                                  game_id=carrinho_request[i].game_id,
                                  vendas_id=venda.id))
    db.add_all(carrinhos)
    db.add_all(games)
    db.commit()


@router.get('')
def listar_venda(usuario: Usuario = Depends(obter_usuario_logado),
                      db: Session = Depends(get_db)):
    vendas = db.query(Venda).filter_by(usuario_id=usuario.id).all()
    historico = []
    for i in range(0, len(vendas)):
        carrinhos = []
        carrinho = db.query(Carrinho).filter_by(vendas_id=vendas[i].id).all()
        for j in range(0, len(carrinho)):
            game = db.query(Game).get(carrinho[j].game_id)
            carrinhos.append(CarrinhoSchema(quantidade=carrinho[j].quantidade, game=game))
        data: datetime = vendas[i].criado_em
        historico.append(VendaResponse(id=vendas[i].id, usuario_id=usuario.id,
                                       carrinhos=carrinhos, valor_total=vendas[i].valor_total,
                                       criado_em=data.strftime("%d/%m/%Y")))
    return historico
