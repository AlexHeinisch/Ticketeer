
def test_get_users_no_authorization_token(client):
    response = client.get('/user')
    assert b'no authorization token provided' in response.data
