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


def test_deve_listar_os_games(instancia_base, json_de_games_para_post):

    client.post('/games', json=json_de_games_para_post)
    client.post('/games', json=json_de_games_para_post)
    game1 = json_de_games_para_post
    game2 = game1.copy()
    game1['id'] = 1
    game2['id'] = 2
    response = client.get('/games')
    assert response.status_code == 200
    assert response.json() == [game1, game2]


def test_deve_retornar_lista_vazia(instancia_base):
    response = client.get('/games')

    assert response.status_code == 200
    assert response.json() == []


def test_deve_criar_um_game(instancia_base, json_de_games_para_post):

    game = json_de_games_para_post
    game_copy = game.copy()
    game_copy['id'] = 1

    response = client.post('/games', json=game)

    assert response.status_code == 201
    assert response.json() == game_copy


def test_deve_excluir_um_game(instancia_base, json_de_games_para_post):
    game_response = client.post('/games', json=json_de_games_para_post)
    response = client.delete(f'/games/{game_response.json()["id"]}')

    assert response.status_code == 204


def test_deve_retornar_404_se_excluir_um_game_com_id_inexistente(instancia_base):
    response = client.delete('/games/12121212121')

    assert response.status_code == 404
    assert response.json()['detail'] == 'Game is not found'


def test_deve_atualizar_um_game(instancia_base, json_de_games_para_post):
    response = client.post('/games', json=json_de_games_para_post)
    id_game = response.json()['id']
    game_put = json_de_games_para_post
    game_put['nome'] = 'Teste Atualizado'
    response_put = client.put(f'/games/{id_game}', json=game_put)

    assert response_put.status_code == 200
    assert response.json()['nome'] != response_put.json()['nome']

