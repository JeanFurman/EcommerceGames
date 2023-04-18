import os
from decimal import Decimal
from enum import Enum
from typing import List

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import uuid

from games_shop.models.games_model import Game
from shared.dependencies import get_db

router = APIRouter(prefix='/games')
diretorio = '/home/jean_/Desktop/Projeto/EcommerceGames/EcommerceGamesAPI/games_shop/images/'


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


class GameRequest(BaseModel):
    nome: str = Field(min_length=3, max_length=80)
    descricao: str = Field(min_length=3, max_length=255)
    genero: GamesGeneroEnum
    desenvolvedor: str = Field(min_length=3, max_length=50)
    plataforma: str = Field(min_length=1, max_length=50)
    valor: Decimal = Field(ge=0)
    quantidade: int = Field(gt=0)


@router.get('', response_model=List[GamesResponse])
def listar_games(db: Session = Depends(get_db)) -> List[GamesResponse]:
    return db.query(Game).all()


@router.get('/{id_game}', response_model=GamesResponse)
def listar_game_por_id(id_game: int, db: Session = Depends(get_db)) -> GamesResponse:
    return buscar_game_por_id(id_game, db)


@router.get('/imagens/{id_imagem}')
def listar_imagens(id_imagem: str):
    try:
        path = f'{diretorio}{id_imagem}'
        return FileResponse(path)
    except:
        raise HTTPException(status_code=404, detail='Imagem não existe')


@router.post('', response_model=GamesResponse, status_code=201)
async def criar_game(nome: str = Form(...), descricao: str = Form(...), genero: str = Form(...),
                     desenvolvedor: str = Form(...), plataforma: str = Form(...),
                     valor: Decimal = Form(...), quantidade: int = Form(...), file: UploadFile = File(...),
                     db: Session = Depends(get_db)) -> GamesResponse:
    game_request = GameRequest(nome=nome, descricao=descricao,
                               genero=genero, desenvolvedor=desenvolvedor,
                               plataforma=plataforma, valor=valor, quantidade=quantidade)
    game = Game(**game_request.dict())
    sufix = os.path.splitext(file.filename)[1]
    file.filename = f'{uuid.uuid4()}{sufix}'
    contents = await file.read()
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
    path = os.path.join(diretorio, game.imagem)
    os.remove(path)
    db.delete(game)
    db.commit()


@router.put('/{id_game}', response_model=GamesResponse, status_code=200)
async def atualizar_game(id_game: int, nome: str = Form(...), descricao: str = Form(...), genero: str = Form(...),
                         desenvolvedor: str = Form(...), plataforma: str = Form(...),
                         valor: Decimal = Form(...), quantidade: int = Form(...), file: UploadFile = File(...),
                         db: Session = Depends(get_db)) -> GamesResponse:
    game_request = GameRequest(nome=nome, descricao=descricao,
                               genero=genero, desenvolvedor=desenvolvedor,
                               plataforma=plataforma, valor=valor, quantidade=quantidade)
    game_att = Game(**game_request.dict())
    game = buscar_game_por_id(id_game, db)
    game.nome = game_att.nome
    game.descricao = game_att.descricao
    game.genero = game_att.genero
    game.desenvolvedor = game_att.desenvolvedor
    game.plataforma = game_att.plataforma
    game.valor = game_att.valor
    game.quantidade = game_att.quantidade
    imagem = game.imagem
    sufix = os.path.splitext(file.filename)[1]
    file.filename = f'{uuid.uuid4()}{sufix}'
    contents = await file.read()
    with open(f'{diretorio}{file.filename}', 'wb') as f:
        f.write(contents)
    game.imagem = file.filename
    if imagem is not None:
        path = os.path.join(diretorio, imagem)
        os.remove(path)
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

