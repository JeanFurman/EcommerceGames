from decimal import Decimal
from enum import Enum
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from games_shop.models.games_model import Game
from shared.dependencies import get_db

router = APIRouter(prefix='/games_shop')


class GamesResponse(BaseModel):
    id: int
    nome: str
    descricao: str
    genero: str
    desenvolvedor: str
    plataforma: str
    valor: Decimal

    class Config:
        orm_mode = True


class GamesGeneroEnum(str, Enum):
    FPS = 'FPS'
    BATTLE_ROYALE = 'BATTLE ROYALE'
    PVP = 'PVP'
    MOBA ='MOBA'
    RPG = 'RPG'
    MMORPG = 'MMORPG'
    AVENTURA = 'AVENTURA'
    CORRIDA = 'CORRIDA'


class GameRequest(BaseModel):
    nome: str = Field(min_length=3, max_length=80)
    descricao: str = Field(min_length=3, max_length=255)
    genero: GamesGeneroEnum
    desenvolvedor: str = Field(min_length=3, max_length=50)
    plataforma: str = Field(min_length=1, max_length=50)
    valor: Decimal = Field(gte=0)


@router.get('', response_model=List[GamesResponse])
def listar_games(db: Session = Depends(get_db)) -> List[GamesResponse]:
    return db.query(Game).all()


@router.post('', response_model=GamesResponse, status_code=201)
def criar_game(game_request: GameRequest, db: Session = Depends(get_db)) -> GamesResponse:
    game = Game(**game_request.dict())
    db.add(game)
    db.commit()
    db.refresh(game)

    return game


@router.delete('/{id_game}', status_code=204)
def deletar_game(id_game: int, db: Session = Depends(get_db)):
    game = buscar_game_por_id(id_game, db)
    db.delete(game)
    db.commit()


@router.put('/{id_game}', response_model=GamesResponse, status_code=200)
def atualizar_game(id_game: int, game_request: GameRequest,
                   db: Session = Depends(get_db)) -> GamesResponse:
    game = buscar_game_por_id(id_game, db)
    game.nome = game_request.nome
    game.descricao = game_request.descricao
    game.genero = game_request.genero
    game.desenvolvedor = game_request.desenvolvedor
    game.plataforma = game_request.plataforma
    game.valor = game_request.valor
    db.add(game)
    db.commit()
    db.refresh(game)
    return game


def buscar_game_por_id(id_game: int, db: Session = Depends(get_db)) -> Game:
    if id_game is not None:
        game = db.query(Game).get(id_game)
        if game is not None:
            return game

    raise HTTPException(status_code=404, detail='Game is not found')




