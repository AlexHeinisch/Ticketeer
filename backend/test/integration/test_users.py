from flask.testing import FlaskClient
import pytest
from scoutsticketservice.models import UserRole
from scoutsticketservice.security.authentication import generate_token

### [GET] '/user<?param=value&...>'

def test_get_all_users(client_with_test_data: FlaskClient, valid_user1_token, 
        user1, user2, admin1, admin2):
    resp = client_with_test_data.get('/user', 
        headers={'Authorization': f'Bearer {valid_user1_token}'}
    )

    ad1 = admin1.to_dict(); del ad1['password']
    ad2 = admin2.to_dict(); del ad2['password']
    us1 = user1.to_dict(); del us1['password']
    us2 = user2.to_dict(); del us2['password']

    assert resp.status_code == 200 # ok
    assert 4 is len(resp.json)
    assert us1 in resp.json
    assert us2 in resp.json
    assert ad1 in resp.json
    assert ad2 in resp.json

def test_get_users_with_user_role(client_with_test_data: FlaskClient, valid_user1_token, 
        user1, user2):
    resp = client_with_test_data.get('/user?role=USER', 
        headers={'Authorization': f'Bearer {valid_user1_token}'}
    )
    us1 = user1.to_dict(); del us1['password']
    us2 = user2.to_dict(); del us2['password']
    
    assert resp.status_code == 200 # ok
    assert 2 is len(resp.json)
    assert us1 in resp.json
    assert us2 in resp.json

def test_get_users_with_admin_role(client_with_test_data: FlaskClient, valid_user1_token, 
        admin1, admin2):
    resp = client_with_test_data.get('/user?role=ADMIN', 
        headers={'Authorization': f'Bearer {valid_user1_token}'}
    )
    ad1 = admin1.to_dict(); del ad1['password']
    ad2 = admin2.to_dict(); del ad2['password']
    
    assert resp.status_code == 200 # ok
    assert 2 is len(resp.json)
    assert ad1 in resp.json
    assert ad2 in resp.json

def test_get_users_by_name_search(client_with_test_data: FlaskClient, valid_user1_token, 
        user2):
    resp = client_with_test_data.get(f'/user?username={user2.username[:-3]}', 
        headers={'Authorization': f'Bearer {valid_user1_token}'}
    )

    us2 = user2.to_dict(); del us2['password']
    
    assert resp.status_code == 200 # ok
    assert 1 is len(resp.json)
    assert us2 == resp.json[0]

def test_get_users_by_email_search(client_with_test_data: FlaskClient, valid_user1_token, 
        user2):
    resp = client_with_test_data.get(f'/user?email={user2.email[3:]}', 
        headers={'Authorization': f'Bearer {valid_user1_token}'}
    )

    us2 = user2.to_dict(); del us2['password']
    
    assert resp.status_code == 200 # ok
    assert 1 is len(resp.json)
    assert us2 == resp.json[0]

def test_get_users_by_email_and_name_search(client_with_test_data: FlaskClient, valid_user1_token, 
        user2):
    resp = client_with_test_data.get(f'/user?email={user2.email[3:]}&username={user2.username[:-3]}', 
        headers={'Authorization': f'Bearer {valid_user1_token}'}
    )
    us2 = user2.to_dict(); del us2['password']

    assert resp.status_code == 200 # ok
    assert 1 is len(resp.json)
    assert us2 == resp.json[0]

def test_get_users_by_random_search(client_with_test_data: FlaskClient, valid_user1_token, 
        user2):
    resp = client_with_test_data.get(f'/user?email={user2.email[3:]}&random=3', 
        headers={'Authorization': f'Bearer {valid_user1_token}'}
    )

    assert resp.status_code == 422 # validation
    assert 'Unknown field.' in resp.json['random']

def test_get_users_no_result_search(client_with_test_data: FlaskClient, valid_user1_token, user2):
    resp = client_with_test_data.get(f'/user?email=xxxxx', 
        headers={'Authorization': f'Bearer {valid_user1_token}'}
    )
    assert resp.status_code == 200 # ok
    assert 0 is len(resp.json)

def test_get_users_no_auth_token(client_with_test_data: FlaskClient):
    resp = client_with_test_data.get(f'/user')
    
    assert resp.status_code == 401 # unauthorized
    assert 'no authorization token provided' in resp.json['errors']

def test_get_users_invalid_auth_token(client_with_test_data: FlaskClient, 
        user1):
    invalid_token = generate_token(user1.username, user1.role, 'IHaveNoIdeaAboutTheSecret')
    resp = client_with_test_data.get(f'/user', 
        headers={'Authorization': f'Bearer {invalid_token}'}
    )
    
    assert resp.status_code == 401 # unauthorized
    assert 'invalid authorization token provided' in resp.json['errors']

### [GET] '/user/<name>'

def test_get_user_by_path(client_with_test_data: FlaskClient, valid_user1_token, user2):
    resp = client_with_test_data.get(f'/user/{user2.username}', 
        headers={'Authorization': f'Bearer {valid_user1_token}'}
    )

    us2 = user2.to_dict(); del us2['password']

    assert resp.status_code == 200 # ok
    assert us2 == resp.json

def test_get_user_by_path_not_found(client_with_test_data: FlaskClient, valid_user1_token):
    resp = client_with_test_data.get(f'/user/xxxx', 
        headers={'Authorization': f'Bearer {valid_user1_token}'}
    )

    assert resp.status_code == 404 # not found

def test_get_user_by_path_no_auth_token(client_with_test_data: FlaskClient, user2):
    resp = client_with_test_data.get(f'/user/{user2.username}')
    assert resp.status_code == 401 # unauthorized
    assert 'no authorization token provided' in resp.json['errors']

def test_get_user_by_path_invalid_auth_token(client_with_test_data: FlaskClient, 
        user1, user2):
    invalid_token = generate_token(user1.username, user1.role, 'IHaveNoIdeaAboutTheSecret')
    resp = client_with_test_data.get(f'/user/{user2.username}', 
        headers={'Authorization': f'Bearer {invalid_token}'}
    )
    
    assert resp.status_code == 401 # unauthorized
    assert 'invalid authorization token provided' in resp.json['errors']

### [POST] '/user'

def test_add_user(client: FlaskClient, user1):
    resp = client.post(f'/user', 
        json={
            "username": user1.username,
            "email": user1.email,
            "password": "hallo123"
        }
    )
    us1 = user1.to_dict(); del us1['password']
    assert resp.status_code is 201 # created
    assert resp.json == us1

def test_add_user_already_exists(client_with_test_data: FlaskClient, user1):
    resp = client_with_test_data.post(f'/user', 
        json={
            "username": user1.username,
            "email": user1.email,
            "password": "hallo123"
        }
    )
    assert resp.status_code == 409 # validation
    assert 'username already in use' in resp.json['errors']

def test_add_user_unknown_field(client: FlaskClient, user1):
    resp = client.post(f'/user', 
        json={
            "username": user1.username,
            "email": user1.email,
            "password": "hallo123",
            "random": 'bonjour'
        }
    )
    assert resp.status_code == 422 # validation
    assert 'Unknown field.' in resp.json['random']

def test_add_user_missing_email(client: FlaskClient, user1):
    resp = client.post(f'/user', 
        json={
            "username": user1.username,
            "password": "hallo123"
        }
    )
    assert resp.status_code == 422 # validation
    assert 'Missing data for required field.' in resp.json['email']

def test_add_user_missing_username(client: FlaskClient, user1):
    resp = client.post(f'/user', 
        json={
            "email": user1.email,
            "password": "hallo123"
        }
    )
    assert resp.status_code == 422 # validation
    assert 'Missing data for required field.' in resp.json['username']

def test_add_user_missing_password(client: FlaskClient, user1):
    resp = client.post(f'/user', 
        json={
            "username": user1.username,
            "email": user1.email
        }
    )
    assert resp.status_code == 422 # validation
    assert 'Missing data for required field.' in resp.json['password']

def test_add_user_empty_username(client: FlaskClient, user1):
    resp = client.post(f'/user', 
        json={
            "username": "",
            "email": user1.email,
            "password": "hallo123"
        }
    )
    assert resp.status_code == 422 # validation
    assert 'Length must be between ' in resp.json['username'][0]

def test_add_user_empty_email(client: FlaskClient, user1):
    resp = client.post(f'/user', 
        json={
            "username": user1.username,
            "email": "",
            "password": "hallo123"
        }
    )
    assert resp.status_code == 422 # validation
    assert 'Not a valid email address.' in resp.json['email'][0]

def test_add_user_invalid_email(client: FlaskClient, user1):
    resp = client.post(f'/user', 
        json={
            "username": user1.username,
            "email": "xxxxx",
            "password": "hallo123"
        }
    )
    assert resp.status_code == 422 # validation
    assert 'Not a valid email address.' in resp.json['email'][0]

def test_add_user_empty_password(client: FlaskClient, user1):
    resp = client.post(f'/user', 
        json={
            "username": user1.username,
            "email": user1.email,
            "password": ""
        }
    )
    assert resp.status_code == 422 # validation
    assert 'Length must be between ' in resp.json['password'][0]

def test_add_user_invalid_data(client: FlaskClient, user1):
    resp = client.post(f'/user', 
        data={
            "random": "not json",
            "beep": 33
        }
    )
    assert resp.status_code == 400 # bad request

### [PATCH] '/user'

def test_patch_user_change_email(client_with_test_data: FlaskClient, user1, valid_user1_token):
    new_mail = 'new.email@example.com'
    resp = client_with_test_data.patch(f'/user/{user1.username}',
        json={
            'email': new_mail
        },
        headers={'Authorization': f'Bearer {valid_user1_token}'}
    )

    us1 = user1.to_dict(); del us1['password']
    us1['email'] = new_mail

    assert resp.status_code == 200 # ok
    assert resp.json == us1

def test_patch_user_change_icon_id(client_with_test_data: FlaskClient, user1, valid_user1_token):
    new_id = 500
    resp = client_with_test_data.patch(f'/user/{user1.username}',
        json={
            'icon_id': new_id
        },
        headers={'Authorization': f'Bearer {valid_user1_token}'}
    )

    us1 = user1.to_dict(); del us1['password']
    us1['icon_id'] = new_id

    assert resp.status_code == 200 # ok
    assert resp.json == us1


def test_patch_user_change_password(client_with_test_data: FlaskClient, user1, valid_user1_token):
    new_password = 'testnewpassword123'
    resp = client_with_test_data.patch(f'/user/{user1.username}',
        json={
            'old_password': user1.password,
            'new_password': new_password
        },
        headers={'Authorization': f'Bearer {valid_user1_token}'}
    )

    us1 = user1.to_dict(); del us1['password']

    assert resp.status_code == 200 # ok
    assert resp.json == us1

    resp = client_with_test_data.patch(f'/user/{user1.username}',
        json={
            'old_password': new_password,
            'new_password': user1.password
        },
        headers={'Authorization': f'Bearer {valid_user1_token}'}
    )

    assert resp.status_code == 200 # ok
    assert resp.json == us1

def test_patch_user_change_password_no_old(client_with_test_data: FlaskClient, user1, valid_user1_token):
    new_password = 'testnewpassword123'
    resp = client_with_test_data.patch(f'/user/{user1.username}',
        json={
            'new_password': new_password
        },
        headers={'Authorization': f'Bearer {valid_user1_token}'}
    )

    us1 = user1.to_dict(); del us1['password']

    assert resp.status_code == 409 # conflict
    assert 'old_password needs to be provided to set the new one' in resp.json['errors']

def test_patch_user_change_password_wrong_old(client_with_test_data: FlaskClient, user1, valid_user1_token):
    new_password = 'testnewpassword123'
    resp = client_with_test_data.patch(f'/user/{user1.username}',
        json={
            'old_password': user1.password + 'nope',
            'new_password': new_password
        },
        headers={'Authorization': f'Bearer {valid_user1_token}'}
    )

    assert resp.status_code == 403 # forbidden
    assert 'could not authenticate' in resp.json['errors']

def test_patch_user_change_icon_id(client_with_test_data: FlaskClient, user1, valid_user1_token):
    new_id = 500
    resp = client_with_test_data.patch(f'/user/{user1.username}',
        json={
            'icon_id': new_id
        },
        headers={'Authorization': f'Bearer {valid_user1_token}'}
    )

    us1 = user1.to_dict(); del us1['password']
    us1['icon_id'] = new_id

    assert resp.status_code == 200 # ok
    assert resp.json == us1

def test_patch_user_change_role_as_self(client_with_test_data: FlaskClient, user1, valid_user1_token):
    new_id = 500
    resp = client_with_test_data.patch(f'/user/{user1.username}',
        json={
            'role': UserRole.ADMIN
        },
        headers={'Authorization': f'Bearer {valid_user1_token}'}
    )

    assert resp.status_code == 403 # ok
    assert 'forbidden' in resp.json['errors']

def test_patch_user_change_role_as_admin(client_with_test_data: FlaskClient, user1, valid_admin1_token):
    resp = client_with_test_data.patch(f'/user/{user1.username}',
        json={
            'role': UserRole.ADMIN
        },
        headers={'Authorization': f'Bearer {valid_admin1_token}'}
    )

    us1 = user1.to_dict(); del us1['password']
    us1['role'] = UserRole.ADMIN.name

    assert resp.status_code == 200 # ok
    assert us1 == resp.json

def test_patch_user_change_role_as_user(client_with_test_data: FlaskClient, user1, valid_user2_token):
    resp = client_with_test_data.patch(f'/user/{user1.username}',
        json={
            'role': UserRole.ADMIN
        },
        headers={'Authorization': f'Bearer {valid_user2_token}'}
    )

    assert resp.status_code == 403 # forbidden
    assert 'forbidden' in resp.json['errors']

def test_patch_user_change_email_of_another_user(client_with_test_data: FlaskClient, user1, valid_user2_token):
    resp = client_with_test_data.patch(f'/user/{user1.username}',
        json={
            'email': 'new.email2@example.com'
        },
        headers={'Authorization': f'Bearer {valid_user2_token}'}
    )

    assert resp.status_code == 403 # forbidden
    assert 'forbidden' in resp.json['errors']

def test_patch_user_change_email_to_invalid(client_with_test_data: FlaskClient, user1, valid_user1_token):
    resp = client_with_test_data.patch(f'/user/{user1.username}',
        json={
            'email': ''
        },
        headers={'Authorization': f'Bearer {valid_user1_token}'}
    )

    assert resp.status_code == 422 # validation
    assert 'Length must be between 1 and 40.' in resp.json['email']

def test_patch_user_change_icon_id_to_invalid(client_with_test_data: FlaskClient, user1, valid_user1_token):
    resp = client_with_test_data.patch(f'/user/{user1.username}',
        json={
            'icon_id': -5
        },
        headers={'Authorization': f'Bearer {valid_user1_token}'}
    )

    assert resp.status_code == 422 # validation
    assert 'Must be greater than or equal to -1.' in resp.json['icon_id']

def test_patch_user_change_role_to_invalid(client_with_test_data: FlaskClient, user1, valid_admin1_token):
    with pytest.deprecated_call(): # marshallow_enum uses deprecated way of throwning errors
        invalid_role = 'NotARole'
        resp = client_with_test_data.patch(f'/user/{user1.username}',
            json={
                'role': invalid_role
            },
            headers={'Authorization': f'Bearer {valid_admin1_token}'}
        )

        assert resp.status_code == 422 # validation
        assert f'Invalid enum value {invalid_role}' in resp.json['role']

def test_patch_user_change_password(client_with_test_data: FlaskClient, user1, valid_user1_token):
    resp = client_with_test_data.patch(f'/user/{user1.username}',
        json={
            'old_password': user1.password,
            'new_password': ''
        },
        headers={'Authorization': f'Bearer {valid_user1_token}'}
    )

    assert resp.status_code == 422 # validation
    assert 'Length must be between 1 and 20.' in resp.json['new_password']

def test_patch_without_username_1(client_with_test_data: FlaskClient, user1, valid_user1_token):
    resp = client_with_test_data.patch(f'/user',
        json={
            'old_password': user1.password,
            'new_password': 'newpassword'
        },
        headers={'Authorization': f'Bearer {valid_user1_token}'}
    )

    assert resp.status_code == 405 # path not allowed

def test_patch_without_username_2(client_with_test_data: FlaskClient, user1, valid_user1_token):
    resp = client_with_test_data.patch(f'/user/',
        json={
            'old_password': user1.password,
            'new_password': 'newpassword'
        },
        headers={'Authorization': f'Bearer {valid_user1_token}'}
    )

    assert resp.status_code == 404 # not found

def test_patch_with_invalid_token(client_with_test_data: FlaskClient, user1):
    resp = client_with_test_data.patch(f'/user/{user1.username}',
        json={
            'old_password': user1.password,
            'new_password': 'newpassword'
        },
        headers={'Authorization': 'Bearer xxxx'}
    )

    assert resp.status_code == 401 # unauthorized
    assert 'invalid authorization token provided' in resp.json['errors']

def test_patch_with_no_token(client_with_test_data: FlaskClient, user1):
    resp = client_with_test_data.patch(f'/user/{user1.username}',
        json={
            'old_password': user1.password,
            'new_password': 'newpassword'
        }
    )

    assert resp.status_code == 401 # unauthorized
    assert 'no authorization token provided' in resp.json['errors']

# [DELETE]

def test_delete_user_with_no_token(client_with_test_data: FlaskClient, user1):
    resp = client_with_test_data.delete(f'/user/{user1.username}')

    assert resp.status_code == 401 # unauthorized
    assert 'no authorization token provided' in resp.json['errors']


def test_delete_other_user_no_admin(client_with_test_data: FlaskClient, user2, valid_user1_token):
    resp = client_with_test_data.delete(f'/user/{user2.username}',
        headers={'Authorization': f'Bearer: {valid_user1_token}'}
    )

    assert resp.status_code == 403 # forbidden
    assert 'forbidden' in resp.json['errors']

def test_delete_self(client_with_test_data: FlaskClient, user1, valid_user1_token):
    resp = client_with_test_data.delete(f'/user/{user1.username}',
        headers={'Authorization': f'Bearer: {valid_user1_token}'}
    )
    assert resp.status_code == 204 # no content
    
    resp = client_with_test_data.get(f'/user/{user1.username}',
        headers={'Authorization': f'Bearer: {valid_user1_token}'}
    )
    assert resp.status_code == 404 # not found

def test_delete_other_user_as_admin(client_with_test_data: FlaskClient, user2, valid_admin1_token):
    resp = client_with_test_data.delete(f'/user/{user2.username}',
        headers={'Authorization': f'Bearer: {valid_admin1_token}'}
    )

    assert resp.status_code == 204 # no content
    
    resp = client_with_test_data.get(f'/user/{user2.username}',
        headers={'Authorization': f'Bearer: {valid_admin1_token}'}
    )
    assert resp.status_code == 404 # not found
