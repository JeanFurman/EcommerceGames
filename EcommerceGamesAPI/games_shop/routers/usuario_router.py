from decimal import Decimal
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from games_shop.models.usuario_model import Usuario
from shared.dependencies import get_db
from games_shop.providers import hash_provider, token_provider
from games_shop.routers.utils import obter_usuario_logado, \
    buscar_usuario_por_email, verificar_email_do_usuario, buscar_usuario_por_id

router = APIRouter(prefix='/usuario')


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str

    class Config:
        orm_mode = True


class UsuarioRequest(BaseModel):
    nome: str = Field(min_length=3, max_length=80)
    email: str = Field()
    senha: str = Field(min_length=3)


class LoginRequest(BaseModel):
    email: str
    senha: str


@router.get('', response_model=List[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)) -> List[UsuarioResponse]:
    return db.query(Usuario).all()


@router.post('/token')
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    senha = login_request.senha
    email = login_request.email

    usuario = buscar_usuario_por_email(email, db)
    if not usuario:
        raise HTTPException(status_code=400, detail='Email ou senha incorretos!')
    try:
        senha_valida = hash_provider.verificar_hash(senha, usuario.senha)
    except:
        raise HTTPException(status_code=400, detail='Email ou senha incorretos!')
    if not senha_valida:
        raise HTTPException(status_code=400, detail='Email ou senha incorretos!')

    token = token_provider.criar_access_token({'sub': usuario.email})
    return {'usuario': usuario, 'access_token': token}


@router.get('/me', response_model=UsuarioResponse)
def me(usuario: Usuario = Depends(obter_usuario_logado)):
    return usuario


@router.post('', response_model=UsuarioResponse, status_code=201)
def criar_usuario(usuario_request: UsuarioRequest, db: Session = Depends(get_db)) -> UsuarioResponse:
    usuario = Usuario(nome=usuario_request.nome
                      , email=verificar_email_do_usuario(usuario_request.email, db)
                      , senha=hash_provider.gerar_hash(usuario_request.senha))
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    return usuario


@router.delete('/{id_usuario}', status_code=204)
def deletar_usuario(id_usuario: int, db: Session = Depends(get_db)):
    usuario = buscar_usuario_por_id(id_usuario, db)
    db.delete(usuario)
    db.commit()


@router.put('/{id_usuario}', response_model=UsuarioResponse, status_code=200)
def atualizar_usuario(id_usuario: int, usuario_request: UsuarioRequest,
                      db: Session = Depends(get_db)) -> UsuarioResponse:
    usuario = buscar_usuario_por_id(id_usuario, db)
    usuario.nome = usuario_request.nome
    usuario.email = usuario_request.email
    usuario.senha = usuario_request.senha
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario
