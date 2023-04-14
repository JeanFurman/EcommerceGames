import os
from decimal import Decimal
from enum import Enum
from typing import List

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import uuid

from games_shop.models.games_model import Game
from shared.dependencies import get_db

router = APIRouter(prefix='/games')


class GamesResponse(BaseModel):
    id: int
    nome: str
    descricao: str
    genero: str
    desenvolvedor: str
    plataforma: str
    imagem: str | None
    valor: Decimal

    class Config:
        orm_mode = True


class GamesGeneroEnum(str, Enum):
    FPS = 'FPS'
    BATTLE_ROYALE = 'BATTLE ROYALE'
    PVP = 'PVP'
    MOBA = 'MOBA'
    RPG = 'RPG'
    MMORPG = 'MMORPG'
    AVENTURA = 'AVENTURA'
    CORRIDA = 'CORRIDA'
    RITMO = 'RITMO'


class GeneroResponse(BaseModel):
    nome: str
    generos: List[GamesGeneroEnum]

    class Config:
        use_enum_values = True


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
async def criar_game(nome: str = Form(...), descricao: str = Form(...), genero: str = Form(...),
                     desenvolvedor: str = Form(...), plataforma: str = Form(...),
                     valor: Decimal = Form(...), file: UploadFile = File(...),
                     db: Session = Depends(get_db)) -> GamesResponse:
    game_request = GameRequest(nome=nome, descricao=descricao,
                               genero=genero, desenvolvedor=desenvolvedor,
                               plataforma=plataforma, valor=valor)
    game = Game(**game_request.dict())
    sufix = os.path.splitext(file.filename)[1]
    file.filename = f'{uuid.uuid4()}{sufix}'
    contents = await file.read()
    diretorio = '/home/jean_/Desktop/Projeto/EcommerceGames/EcommerceGamesAPI/games_shop/images/'
    with open(f'{diretorio}{file.filename}', 'wb') as f:
        f.write(contents)
    game.imagem = file.filename
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
