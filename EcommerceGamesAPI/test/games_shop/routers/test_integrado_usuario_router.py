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
def json_de_usuario_para_post():

    return {
            'nome': 'Teste nome',
            'email': 'teste@gmail.com',
            'senha': 'abc123',
            }


def test_deve_listar_o_usuario_por_token(instancia_base, json_de_usuario_para_post):
    client.post('/usuario', json=json_de_usuario_para_post)
    response_login = client.post('usuario/token', json={
        'email': 'teste@gmail.com',
        'senha': 'abc123'
    })
    usuario = {
                'id': 1,
                'nome': 'Teste nome',
                'email': 'teste@gmail.com',
                }
    usuario_get = client.get('/usuario', headers={
        'Authorization': f'Bearer {response_login.json()["access_token"]}'
    })

    assert usuario_get.json() == usuario


def test_deve_retornar_lista_vazia(instancia_base):
    response = client.get('/usuario')

    assert response.status_code == 200
    assert response.json() == []


def test_deve_criar_um_usuario(instancia_base, json_de_usuario_para_post):

    usuario = json_de_usuario_para_post
    usuario_copy = usuario.copy()
    usuario_copy['id'] = 1
    del usuario_copy['senha']

    response = client.post('/usuario', json=usuario)

    assert response.status_code == 201
    assert response.json() == usuario_copy


def test_deve_excluir_um_usuario(instancia_base, json_de_usuario_para_post):
    usuario_response = client.post('/usuario', json=json_de_usuario_para_post)
    response = client.delete(f'/usuario/{usuario_response.json()["id"]}')

    assert response.status_code == 204


def test_deve_retornar_404_se_excluir_um_usuario_com_id_inexistente(instancia_base):
    response = client.delete('/usuario/12121212121')

    assert response.status_code == 404
    assert response.json()['detail'] == 'Usuario is not found'


def test_deve_atualizar_um_usuario(instancia_base, json_de_usuario_para_post):
    response = client.put('/usuario', json=json_de_usuario_para_post)
    id_usuario = response.json()['id']
    usuario_put = json_de_usuario_para_post
    usuario_put['nome'] = 'Teste Atualizado'
    response_put = client.put(f'/usuario/{id_usuario}', json=usuario_put)

    assert response_put.status_code == 200
    assert response.json()['nome'] != response_put.json()['nome']


def test_deve_fazer_login(instancia_base, json_de_usuario_para_post):
    client.post('/usuario', json=json_de_usuario_para_post)
    response_login = client.post('usuario/token', json={
        'email': 'teste@gmail.com',
        'senha': 'abc123'
    })

    assert response_login.status_code == 200
    assert response_login.json()['access_token'] != ''


def test_deve_dar_excecao_quando_fizer_login_com_senha_ou_email_errados(instancia_base, json_de_usuario_para_post):
    client.post('/usuario', json=json_de_usuario_para_post)
    response_login = client.post('usuario/token', json={
        'email': 'teste@gmail.com',
        'senha': 'senhaErrada'
    })

    assert response_login.status_code == 400

    response_login = client.post('usuario/token', json={
        'email': 'emailErrado@gmail.com',
        'senha': 'abc123'
    })

    assert response_login.status_code == 400


def test_deve_conseguir_acessar_me(instancia_base, json_de_usuario_para_post):
    client.post('/usuario', json=json_de_usuario_para_post)
    response_login = client.post('usuario/token', json={
        'email': 'teste@gmail.com',
        'senha': 'abc123'
    })
    token = response_login.json()['access_token']
    response_get = client.get('/usuario/me', headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    })

    assert response_get.status_code == 200
    assert response_get.json()['nome'] == 'Teste'


def test_nao_deve_conseguir_acessar_me(instancia_base, json_de_usuario_para_post):
    token = '4b6b3852c691a39b9eba0901c262dcc96194d78e713f490fe0bf964fde98e3f4'
    response_get = client.get('/usuario/me', headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    })

    assert response_get.status_code == 401
