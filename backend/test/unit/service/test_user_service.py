
import pytest
from werkzeug.security import check_password_hash, generate_password_hash
from ticketeer.dto.dtos import LoginRequestDto, UserRegisterRequestDto, UserRole, UserSearchRequestDto, UserUpdateRequestDto
from ticketeer.error.custom_errors import ConflictError, NotFoundError, PermissionError
from ticketeer.models import User
from ticketeer.security.authorization import CurrentPermissions
from ticketeer.service.user_service import UserService


def test_insert_user_success(
        mock_repository,
        user_service: UserService,
        sample_user: User,
        sample_user_password: str
    ):
    mock_repository.get_user_by_name.return_value = None
    mock_repository.insert_user.return_value = User.to_dto(sample_user)

    req = UserRegisterRequestDto(
        username=sample_user.username, 
        email=sample_user.email, 
        password=sample_user_password
    )
    returned_user = user_service.register_user(req)
    assert returned_user == User.to_dto(sample_user)
    mock_repository.get_user_by_name.assert_called_once_with(req.username)
    mock_repository.insert_user.assert_called_once_with(req)

def test_insert_user_already_exists(
        mock_repository,
        user_service: UserService,
        sample_user: User,
        sample_user_password: str
    ):
    mock_repository.get_user_by_name.return_value = User.to_dto(sample_user)

    req = UserRegisterRequestDto(
        username=sample_user.username, 
        email=sample_user.email, 
        password=sample_user_password
    )
    with pytest.raises(ConflictError) as err_info:
        user_service.register_user(req)
    assert 'username already in use' in str(err_info.value)
    mock_repository.get_user_by_name.assert_called_once_with(req.username)
    assert not mock_repository.insert_user.called

def test_get_user_by_name_success(
    mock_repository,
    user_service: UserService,
    sample_user: User
    ):
    mock_repository.get_user_by_name.return_value = User.to_dto(sample_user)

    returned_user = user_service.get_user_by_name(sample_user.username)
    assert User.to_dto(sample_user) == returned_user
    mock_repository.get_user_by_name.assert_called_once_with(sample_user.username)

def test_get_user_by_name_not_found(
    mock_repository,
    user_service: UserService,
    sample_user: User
    ):
    mock_repository.get_user_by_name.return_value = None

    with pytest.raises(NotFoundError) as err_info:
        user_service.get_user_by_name(sample_user.username)
    assert 'given user does not exist' in str(err_info.value)
    mock_repository.get_user_by_name.assert_called_once_with(sample_user.username)

def test_get_user_by_id_success(
    mock_repository,
    user_service: UserService,
    sample_user: User
    ):
    mock_repository.get_user_by_id.return_value = User.to_dto(sample_user)

    returned_user = user_service.get_user_by_id(sample_user.id)
    assert User.to_dto(sample_user) == returned_user
    mock_repository.get_user_by_id.assert_called_once_with(sample_user.id)

def test_get_user_by_id_not_found(
    mock_repository,
    user_service: UserService,
    sample_user: User
    ):
    mock_repository.get_user_by_id.return_value = None

    with pytest.raises(NotFoundError) as err_info:
        user_service.get_user_by_id(sample_user.id)
    assert 'given user does not exist' in str(err_info.value)
    mock_repository.get_user_by_id.assert_called_once_with(sample_user.id)

def test_delete_user_by_name_success(
    mock_repository,
    user_service: UserService,
    sample_user: User
    ):
    mock_repository.get_user_by_name.return_value = User.to_dto(sample_user)

    user_service.delete_user_by_name(sample_user.username)
    mock_repository.delete_user_by_name.assert_called_once_with(sample_user.username)
    mock_repository.get_user_by_name.assert_called_once_with(sample_user.username)

def test_delete_user_by_name_not_found(
    mock_repository,
    user_service: UserService,
    sample_user: User
    ):
    mock_repository.get_user_by_name.return_value = None

    with pytest.raises(NotFoundError) as err_info:
        user_service.delete_user_by_name(sample_user.username)
    assert 'given user does not exist' in str(err_info.value)
    assert not mock_repository.delete_user_by_name.called
    mock_repository.get_user_by_name.assert_called_once_with(sample_user.username)

def test_delete_user_by_id_success(
    mock_repository,
    user_service: UserService,
    sample_user: User
    ):
    mock_repository.get_user_by_id.return_value = User.to_dto(sample_user)

    user_service.delete_user_by_id(sample_user.id)
    mock_repository.delete_user_by_id.assert_called_once_with(sample_user.id)
    mock_repository.get_user_by_id.assert_called_once_with(sample_user.id)

def test_delete_user_by_id_not_found(
    mock_repository,
    user_service: UserService,
    sample_user: User
    ):
    mock_repository.get_user_by_id.return_value = None

    with pytest.raises(NotFoundError) as err_info:
        user_service.delete_user_by_id(sample_user.id)
    assert 'given user does not exist' in str(err_info.value)
    assert not mock_repository.delete_user_by_id.called
    mock_repository.get_user_by_id.assert_called_once_with(sample_user.id)

def test_verify_login_success(
    mock_repository,
    user_service: UserService,
    sample_user: User,
    sample_user_password: str
    ):
    mock_repository.get_user_by_name.return_value = User.to_dto(sample_user)

    req = LoginRequestDto(sample_user.username, sample_user_password)
    assert user_service.verify_login(req)
    mock_repository.get_user_by_name.assert_called_once_with(sample_user.username)

def test_verify_login_wrong_password(
    mock_repository,
    user_service: UserService,
    sample_user: User,
    sample_user_password: str
    ):
    mock_repository.get_user_by_name.return_value = User.to_dto(sample_user)

    req = LoginRequestDto(sample_user.username, f'{sample_user_password}xxx')
    assert not user_service.verify_login(req)
    mock_repository.get_user_by_name.assert_called_once_with(sample_user.username)

def test_verify_login_user_not_found(
    mock_repository,
    user_service: UserService,
    sample_user: User,
    sample_user_password: str
    ):
    mock_repository.get_user_by_name.return_value = None

    req = LoginRequestDto(sample_user.username, sample_user_password)
    assert not user_service.verify_login(req)
    mock_repository.get_user_by_name.assert_called_once_with(sample_user.username)

def test_get_multiple_users(
    mock_repository,
    user_service: UserService,
    sample_user: User,
    ):
    mock_repository.get_users_by_search_req.return_value = [User.to_dto(sample_user)]

    req = UserSearchRequestDto(username='xxx')
    returned_users = user_service.get_multiple_users(req)
    assert len(returned_users) == 1
    assert User.to_dto(sample_user) in returned_users
    mock_repository.get_users_by_search_req.assert_called_once_with(req)

def test_update_user_not_found(
    mock_repository,
    user_service: UserService,
    sample_user: User,
    ):
    mock_repository.get_user_by_id.return_value = None

    req = UserUpdateRequestDto(-5, username='NewName')
    perm = CurrentPermissions(id=sample_user.id, user_name=sample_user.username, user_role=sample_user.role) 

    with pytest.raises(NotFoundError) as err_info:
        user_service.update_user(req, perm)
    assert 'given user does not exist' in str(err_info.value)
    mock_repository.get_user_by_id.assert_called_once_with(-5)
    assert not mock_repository.update_user.called
    
def test_update_user_normal_user_tries_role_change(
    mock_repository,
    user_service: UserService,
    sample_user: User,
    ):
    mock_repository.get_user_by_id.return_value = User.to_dto(sample_user)

    req = UserUpdateRequestDto(id=sample_user.id, role=UserRole.ADMIN) 
    perm = CurrentPermissions(id=sample_user.id, user_name=sample_user.username, user_role=sample_user.role) 
   
    with pytest.raises(PermissionError) as err_info:
        user_service.update_user(req, perm)
    assert 'forbidden' in str(err_info.value)
    assert not mock_repository.update_user.called

def test_update_user_newpass_without_oldpass(
    mock_repository,
    user_service: UserService,
    sample_user: User,
    ):
    mock_repository.get_user_by_id.return_value = User.to_dto(sample_user)

    req = UserUpdateRequestDto(id=sample_user.id, new_password='newpass123') 
    perm = CurrentPermissions(id=sample_user.id, user_name=sample_user.username, user_role=sample_user.role) 
   
    with pytest.raises(ConflictError) as err_info:
        user_service.update_user(req, perm)
    assert 'old_password needs to be provided' in str(err_info.value)
    assert not mock_repository.update_user.called

def test_update_user_newpass_with_wrong_oldpass(
    mock_repository,
    user_service: UserService,
    sample_user: User,
    ):
    mock_repository.get_user_by_name.return_value = User.to_dto(sample_user)

    req = UserUpdateRequestDto(id=sample_user.id, new_password='newpass123', old_password='wrongpass123') 
    perm = CurrentPermissions(id=sample_user.id, user_name=sample_user.username, user_role=sample_user.role) 
   
    with pytest.raises(PermissionError) as err_info:
        user_service.update_user(req, perm)
    assert 'could not authenticate' in str(err_info.value)
    assert not mock_repository.update_user.called

def test_update_user_success(
    mock_repository,
    user_service: UserService,
    sample_user: User,
    sample_user_password: str
    ):
    new_pw = 'imanewpassword123'
    mock_repository.get_user_by_name.return_value = User.to_dto(sample_user)
    mock_repository.update_user.return_value = User.to_dto(sample_user)

    req = UserUpdateRequestDto(id=sample_user.id, new_password=new_pw, old_password=sample_user_password) 
    perm = CurrentPermissions(id=sample_user.id, user_name=sample_user.username, user_role=sample_user.role) 
   
    returned_user = user_service.update_user(req, perm)
    assert User.to_dto(sample_user) == returned_user
    assert req.new_password and check_password_hash(req.new_password, new_pw)
    


