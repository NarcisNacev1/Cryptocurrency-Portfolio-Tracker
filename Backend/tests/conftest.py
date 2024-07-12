import json
import pytest
from Backend.src import create_app, db
from Backend.src.models import User


@pytest.fixture(scope='module')
def test_client():
    app = create_app()
    testing_client = app.test_client('Backend.src.config.config')

    ctx = app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture(scope='module')
def init_database():

    db.create_all()

    user = User(username='testuser')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()

    yield db

    db.session.close()
    db.drop_all()


def get_jwt_token(test_client):
    response = test_client.post('/login',
                                data=json.dumps({'username': 'testuser', 'password': 'password'}),
                                content_type='application/json')
    data = json.loads(response.data)
    return data['access_token']
