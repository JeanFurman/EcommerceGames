from decimal import Decimal
from enum import Enum
from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from games.models.games_model import Games
from shared.dependencies import get_db

router = APIRouter(prefix='/games')


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
    return db.query(Games).all()


@router.post('', response_model=GamesResponse, status_code=201)
def criar_game(game_request: GameRequest, db: Session = Depends(get_db)) -> GamesResponse:
    game = Games(**game_request.dict())
    db.add(game)
    db.commit()
    db.refresh(game)

    return game



