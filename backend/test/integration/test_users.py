import pytest

@pytest.mark.parametrize('client_name',[
                             pytest.param('level1_client', marks=pytest.mark.dependency(name='l1_test_1')),
                             pytest.param('level2_client', marks=pytest.mark.dependency(name='l2_test_1', depends=['l1_test_1'])),
                             pytest.param('level3_client', marks=pytest.mark.dependency(name='l3_test_1', depends=['l2_test_1'])),
                             pytest.param('level4_client', marks=pytest.mark.dependency(name='l4_test_1', depends=['l3_test_1'])),
                         ])
def test_1_get_users_no_authorization_token(client_name, request):
    client = request.getfixturevalue(client_name)
    response = client.get('/user')
    assert b'no authorization token provided' in response.data
