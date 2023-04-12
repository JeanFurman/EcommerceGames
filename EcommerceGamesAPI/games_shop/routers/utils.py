from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException

from games_shop.models.usuario_model import Usuario
from shared.dependencies import get_db
from sqlalchemy.orm import Session
from games_shop.providers import token_provider
from jose import JWTError

from email_validator import validate_email, EmailNotValidError

oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')


def obter_usuario_logado(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    exception = HTTPException(status_code=401, detail='Token inválido')

    try:
        email = token_provider.verificar_access_token(token)
    except JWTError:
        raise exception

    if not email:
        raise exception

    usuario = buscar_usuario_por_email(email, db)

    if not usuario:
        raise exception

    return usuario


def buscar_usuario_por_id(id_usuario: int, db: Session = Depends(get_db)) -> Usuario:
    if id_usuario is not None:
        usuario = db.query(Usuario).get(id_usuario)
        if usuario is not None:
            return usuario

    raise HTTPException(status_code=404, detail='Usuario is not found')


def buscar_usuario_por_email(email_usuario: str, db: Session = Depends(get_db)) -> Usuario | None:
    return db.query(Usuario).filter_by(email=email_usuario).first()


def verificar_email_do_usuario(email_usuario: str, db: Session = Depends(get_db)) -> str:
    if email_usuario is not None:
        try:
            validation = validate_email(email_usuario, check_deliverability=True)
            usuario = buscar_usuario_por_email(validation.email, db)
        except EmailNotValidError:
            raise HTTPException(status_code=404, detail='Email inválido!')
        if usuario is None:
            return email_usuario
        else:
            raise HTTPException(status_code=400, detail='Email ja cadastrado!')

    raise HTTPException(status_code=404, detail='O campo Email é obrigatório!')


