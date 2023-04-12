from decimal import Decimal
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy.orm import Session

from games_shop.models.usuario_model import Usuario
from shared.dependencies import get_db
from games_shop.providers import hash_provider

from email_validator import validate_email, EmailNotValidError

router = APIRouter(prefix='/usuario')


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    senha: str

    class Config:
        orm_mode = True


class UsuarioRequest(BaseModel):
    nome: str = Field(min_length=3, max_length=80)
    email: str = EmailStr()
    senha: str = Field(min_length=3)


@router.get('', response_model=List[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)) -> List[UsuarioResponse]:
    return db.query(Usuario).all()


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


def buscar_usuario_por_id(id_usuario: int, db: Session = Depends(get_db)) -> Usuario:
    if id_usuario is not None:
        usuario = db.query(Usuario).get(id_usuario)
        if usuario is not None:
            return usuario

    raise HTTPException(status_code=404, detail='Usuario is not found')


def verificar_email_do_usuario(email_usuario: str, db: Session = Depends(get_db)) -> str:
    if email_usuario is not None:
        try:
            validation = validate_email(email_usuario, check_deliverability=True)
            usuario = db.query(Usuario).filter_by(email=validation.email).first()
        except EmailNotValidError:
            raise HTTPException(status_code=404, detail='Email inválido!')
        if usuario is None:
            return email_usuario
        else:
            raise HTTPException(status_code=400, detail='Email ja cadastrado!')

    raise HTTPException(status_code=404, detail='O campo Email é obrigatório!')
