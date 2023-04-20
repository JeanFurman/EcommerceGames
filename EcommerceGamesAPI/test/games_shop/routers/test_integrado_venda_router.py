from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pytest import fixture
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


@fixture(scope='function')
def instancia_base():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@fixture(scope='function')
def json_de_games_para_post():
    return {
            'nome': 'Teste nome',
            'descricao': 'Teste descricao',
            'genero': 'FPS',
            'desenvolvedor': 'Teste desenvolvedor',
            'plataforma': 'Teste plataforma',
            'valor': 10,
            }





def test_deve_criar_um_game(instancia_base, json_de_games_para_post):

    game = json_de_games_para_post
    game_copy = game.copy()
    game_copy['id'] = 1

    response = client.post('/games', json=game)

    assert response.status_code == 201
    assert response.json() == game_copy



