import pytest
from ticketeer import db
from ticketeer.dto.schemas import UserSchema
from ticketeer.models import User

@pytest.fixture(scope='function')
def client_with_sample_users(sample_user, sample_user2, sample_admin, app, client):
    with app.app_context():
        db.session.add(sample_user)
        db.session.add(sample_user2)
        db.session.add(sample_admin)
        db.session.commit()
        yield client

def test_get_users_no_authorization_token(client):
    response = client.get('/user')
    assert b'no authorization token provided' in response.data

def test_get_users_success(
        client_with_sample_users, 
        sample_user_token, 
        sample_user, 
        sample_user2, 
        sample_admin
    ):
    response = client_with_sample_users.get(
        '/user', 
        headers={
            "authorization": f'Bearer {sample_user_token}'
        }
    )
    assert '200' in response.status
    assert len(response.json) == 3
    assert UserSchema().dump(User.to_dto(sample_user)) in response.json
    assert UserSchema().dump(User.to_dto(sample_user2)) in response.json
    assert UserSchema().dump(User.to_dto(sample_admin)) in response.json

