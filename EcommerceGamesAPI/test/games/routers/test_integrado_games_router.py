from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from shared.database import Base
from shared.dependencies import get_db

client = TestClient(app)

SQLALCHEMY_DATABASE_URL = 'sqlite:///./test.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def test_deve_listar_os_games():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    client.post('/games', json={
        'nome': 'Teste nome',
        'descricao': 'Teste descricao',
        'genero': 'FPS',
        'desenvolvedor': 'Teste desenvolvedor',
        'plataforma': 'Teste plataforma',
        'valor': 10,
    })
    client.post('/games', json={
        'nome': 'Teste nome 2',
        'descricao': 'Teste descricao 2',
        'genero': 'FPS',
        'desenvolvedor': 'Teste desenvolvedor 2',
        'plataforma': 'Teste plataforma 2',
        'valor': 10,
    })
    response = client.get('/games')

    assert response.status_code == 200
    assert response.json() == [
        {
            'id': 1,
            'nome': 'Teste nome',
            'descricao': 'Teste descricao',
            'genero': 'FPS',
            'desenvolvedor': 'Teste desenvolvedor',
            'plataforma': 'Teste plataforma',
            'valor': 10,
        },
        {
            'id': 2,
            'nome': 'Teste nome 2',
            'descricao': 'Teste descricao 2',
            'genero': 'FPS',
            'desenvolvedor': 'Teste desenvolvedor 2',
            'plataforma': 'Teste plataforma 2',
            'valor': 10,
        }
    ]


def test_deve_retornar_lista_vazia():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    response = client.get('/games')

    assert response.status_code == 200
    assert response.json() == []


def test_deve_criar_um_game():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    game ={
        'nome': 'Teste nome',
        'descricao': 'Teste descricao',
        'genero': 'FPS',
        'desenvolvedor': 'Teste desenvolvedor',
        'plataforma': 'Teste plataforma',
        'valor': 10,
    }
    game_copy = game.copy()
    game_copy['id'] = 1

    response = client.post('/games', json=game)

    assert response.status_code == 201
    assert response.json() == game_copy

