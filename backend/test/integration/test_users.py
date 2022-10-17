import json
import pytest
from ticketeer import db
from ticketeer.dto.dtos import UserRole
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

def test_no_authorization_token(client):
    response = client.get('/user')
    assert '401' in response.status
    assert b'no authorization token provided' in response.data

def test_invalid_authorization_token(
        client
    ):
    response = client.get(
        '/user', 
        headers={
            "authorization": f'Bearer xyzayyyo'
        }
    )
    assert '401' in response.status
    assert b'invalid authorization token provided' in response.data

def test_get_single_user_permission_required(
        client_with_sample_users, 
        sample_user, 
    ):
    response = client_with_sample_users.get(
        f'/user/{sample_user.id}', 
    )
    assert '401' in response.status
    assert b'no authorization token provided' in response.data

def test_get_single_user(
        client_with_sample_users, 
        sample_user_token, 
        sample_user, 
    ):
    response = client_with_sample_users.get(
        f'/user/{sample_user.id}', 
        headers={
            "authorization": f'Bearer {sample_user_token}'
        }
    )
    assert '200' in response.status
    assert UserSchema().dump(User.to_dto(sample_user)) == response.json

def test_get_single_user_not_found(
        client_with_sample_users, 
        sample_user_token 
    ):
    response = client_with_sample_users.get(
        f'/user/111', 
        headers={
            "authorization": f'Bearer {sample_user_token}'
        }
    )
    assert '404' in response.status
    assert b'given user does not exist' in response.data

def test_get_users_permission_required(
        client_with_sample_users, 
    ):
    response = client_with_sample_users.get(
        '/user', 
    )
    assert '401' in response.status
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

def test_get_users_with_limit(
    client_with_sample_users,
    sample_user_token
    ):
    response = client_with_sample_users.get(
        '/user?num=1',
        headers={
            'authorization': f'Bearer {sample_user_token}'
        }
    )
    assert '200' in response.status
    assert len(response.json) == 1

def test_get_users_with_offset(
    client_with_sample_users,
    sample_user_token
    ):
    response = client_with_sample_users.get(
        '/user?num=1',
        headers={
            'authorization': f'Bearer {sample_user_token}'
        }
    )
    response2 = client_with_sample_users.get(
        '/user?num=1&offset=1',
        headers={
            'authorization': f'Bearer {sample_user_token}'
        }
    )
    assert '200' in response.status
    assert '200' in response2.status
    assert len(response.json) == 1
    assert len(response2.json) == 1
    assert response.json[0] != response2.json[0]

def test_get_users_by_username(
    client_with_sample_users,
    sample_user_token,
    sample_admin
    ):
    response = client_with_sample_users.get(
        f'/user?username={sample_admin.username[0:-2]}',
        headers={
            'authorization': f'Bearer {sample_user_token}'
        }
    )
    assert '200' in response.status
    assert len(response.json) == 1
    assert UserSchema().dump(User.to_dto(sample_admin)) in response.json

def test_get_users_by_email(
    client_with_sample_users,
    sample_user_token,
    sample_user2
    ):
    response = client_with_sample_users.get(
        f'/user?email={sample_user2.email[0:-5]}',
        headers={
            'authorization': f'Bearer {sample_user_token}'
        }
    )
    assert '200' in response.status
    assert len(response.json) == 1
    assert UserSchema().dump(User.to_dto(sample_user2)) in response.json

def test_get_users_by_role(
    client_with_sample_users,
    sample_user_token,
    sample_user,
    sample_user2,
    sample_admin
    ):
    response = client_with_sample_users.get(
        f'/user?role={UserRole.USER.name}',
        headers={
            'authorization': f'Bearer {sample_user_token}'
        }
    )
    assert '200' in response.status
    assert len(response.json) == 2
    assert UserSchema().dump(User.to_dto(sample_user2)) in response.json
    assert UserSchema().dump(User.to_dto(sample_user)) in response.json
    assert UserSchema().dump(User.to_dto(sample_admin)) not in response.json

def test_post_user_success(
    client_with_sample_users
    ):
    response = client_with_sample_users.post(
        '/user',
        content_type='application/json',
        data=json.dumps({
            'username': 'max',
            'email': 'mm@example.com',
            'password': 'hallo123'
        })
    )
    assert '201' in response.status
    assert response.json['username'] == 'max'
    assert response.json['email'] == 'mm@example.com'
    assert 'password' not in response.json
    assert response.json['id'] > -1
    assert response.json['role'] == UserRole.USER.name

def test_post_user_already_exists(
    client_with_sample_users,
    sample_user
    ):
    response = client_with_sample_users.post(
        '/user',
        content_type='application/json',
        data=json.dumps({
            'username': sample_user.username,
            'email': 'mm@example.com',
            'password': 'hallo123'
        })
    )
    assert '409' in response.status
    assert b'username already in use' in response.data

def test_delete_user_permissions_required(
    client_with_sample_users
    ):
    response = client_with_sample_users.delete(
        '/user/1'
    )
    assert '401' in response.status
    assert b'no authorization token provided' in response.data

def test_delete_user_try_delete_other_as_normal(
    client_with_sample_users,
    sample_user_token,
    sample_user2
    ):
    response = client_with_sample_users.delete(
        f'/user/{sample_user2.id}',
        headers={
            'authorization': f'Bearer {sample_user_token}'
        }
    )
    assert '403' in response.status
    assert b'forbidden' in response.data

def test_delete_user_as_admin(
    client_with_sample_users,
    sample_admin_token,
    sample_user
    ):
    response = client_with_sample_users.delete(
        f'/user/{sample_user.id}',
        headers={
            'authorization': f'Bearer {sample_admin_token}'
        }
    )
    assert '204' in response.status

def test_delete_user_as_admin_not_found(
    client_with_sample_users,
    sample_admin_token,
    ):
    response = client_with_sample_users.delete(
        f'/user/111',
        headers={
            'authorization': f'Bearer {sample_admin_token}'
        }
    )
    assert '404' in response.status
    assert b'given user does not exist' in response.data

def test_delete_user_self(
    client_with_sample_users,
    sample_user_token,
    sample_user
    ):
    response = client_with_sample_users.delete(
        f'/user/{sample_user.id}',
        headers={
            'authorization': f'Bearer {sample_user_token}'
        }
    )
    assert '204' in response.status

def test_patch_user_permissions_required(
    client_with_sample_users,
    sample_user
    ):
    response = client_with_sample_users.patch(
        f'/user/{sample_user.id}',
        data=json.dumps({
            'email': 'newmail@example.com'
        })
    )
    assert '401' in response.status
    assert b'no authorization token provided' in response.data

def test_patch_user_try_patch_other(
    client_with_sample_users,
    sample_user_token,
    sample_user2
    ):
    response = client_with_sample_users.patch(
        f'/user/{sample_user2.id}',
        headers={
            'authorization': f'Bearer {sample_user_token}'
        },
        data=json.dumps({
            'email': 'newmail@example.com'
        })
    )
    assert '403' in response.status
    assert b'forbidden' in response.data

def test_patch_user_email_as_admin(
    client_with_sample_users,
    sample_admin_token,
    sample_user2
    ):
    response = client_with_sample_users.patch(
        f'/user/{sample_user2.id}',
        headers={
            'authorization': f'Bearer {sample_admin_token}'
        },
        content_type='application/json',
        data=json.dumps({
            'email': 'newmail@example.com'
        })
    )
    assert '200' in response.status
    assert response.json['email'] == 'newmail@example.com'

def test_patch_user_password_as_admin(
    client_with_sample_users,
    sample_admin_token,
    sample_user2
    ):
    response = client_with_sample_users.patch(
        f'/user/{sample_user2.id}',
        headers={
            'authorization': f'Bearer {sample_admin_token}'
        },
        content_type='application/json',
        data=json.dumps({
            'new_password': 'asdf1234'
        })
    )
    assert '200' in response.status

def test_patch_user_password_self_no_old(
    client_with_sample_users,
    sample_user_token,
    sample_user
    ):
    response = client_with_sample_users.patch(
        f'/user/{sample_user.id}',
        headers={
            'authorization': f'Bearer {sample_user_token}'
        },
        content_type='application/json',
        data=json.dumps({
            'new_password': 'asdf1234'
        })
    )
    assert '409' in response.status
    assert b'old_password needs to be provided' in response.data

def test_patch_user_password_self_success(
    client_with_sample_users,
    sample_user_token,
    sample_user,
    sample_user_password
    ):
    response = client_with_sample_users.patch(
        f'/user/{sample_user.id}',
        headers={
            'authorization': f'Bearer {sample_user_token}'
        },
        content_type='application/json',
        data=json.dumps({
            'new_password': 'asdf1234',
            'old_password': sample_user_password 
        })
    )
    assert '200' in response.status

def test_patch_user_email(
    client_with_sample_users,
    sample_user_token,
    sample_user
    ):
    response = client_with_sample_users.patch(
        f'/user/{sample_user.id}',
        headers={
            'authorization': f'Bearer {sample_user_token}'
        },
        content_type='application/json',
        data=json.dumps({
            'email': 'newmail@example.com',
        })
    )
    assert '200' in response.status
    assert response.json['email'] == 'newmail@example.com'

def test_patch_user_username(
    client_with_sample_users,
    sample_user_token,
    sample_user
    ):
    response = client_with_sample_users.patch(
        f'/user/{sample_user.id}',
        headers={
            'authorization': f'Bearer {sample_user_token}'
        },
        content_type='application/json',
        data=json.dumps({
            'username': 'newname',
        })
    )
    assert '200' in response.status
    assert response.json['username'] == 'newname'

def test_patch_user_role_as_user(
    client_with_sample_users,
    sample_user_token,
    sample_user
    ):
    response = client_with_sample_users.patch(
        f'/user/{sample_user.id}',
        headers={
            'authorization': f'Bearer {sample_user_token}'
        },
        content_type='application/json',
        data=json.dumps({
            'role': UserRole.ADMIN,
        })
    )
    assert '403' in response.status
    assert b'forbidden' in response.data

def test_patch_user_role_as_admin(
    client_with_sample_users,
    sample_admin_token,
    sample_user
    ):
    response = client_with_sample_users.patch(
        f'/user/{sample_user.id}',
        headers={
            'authorization': f'Bearer {sample_admin_token}'
        },
        content_type='application/json',
        data=json.dumps({
            'role': UserRole.ADMIN,
        })
    )
    assert '200' in response.status
    assert response.json['role'] == UserRole.ADMIN.name
