import logging
from ..base_daos import TicketDao, UserDao

from injector import inject
from ..connectors.psql_connector import PostgresConnector

from ...models import User, UserSearchRequest, UserUpdateRequest

class PostgresTicketDao(TicketDao):

    @inject
    def __init__(self, connector: PostgresConnector) -> None:
        super().__init__()
        self._connector = connector

    def get(self):
        return 'PostgresTicketDao'

class PostgresUserDao(UserDao):

    @inject
    def __init__(self, connector: PostgresConnector) -> None:
        super().__init__()
        self._connector = connector
        self._logger = logging.getLogger(__name__)

    def get_user_by_name(self, name: str) -> User | None:
        self._logger.debug(f'[persistence] get_user_by_name: name={name}')
        with self._connector.get_conn().cursor() as cur:
            cur.execute(f'SELECT * FROM users WHERE username=\'{name}\';')
            for r in cur:
                return User(*r)
        return None
    
    def get_users_by_search_req(self, req: UserSearchRequest) -> list[User]:
        self._logger.error(f'[persistence] get_users_by_search_req: req={req}')
        res = []
        conditions = []

        if req.email:
            conditions.append(f'LOWER(email) LIKE \'%{req.email.lower()}%\'')
        if req.username:
            conditions.append(f'LOWER(username) LIKE \'%{req.username.lower()}%\'')
        if req.role:
            conditions.append(f'role=\'{req.role.name}\'')
        if len(conditions) is 0:
            conditions.append('1=1')

        with self._connector.get_conn().cursor() as cur:
            cur.execute(f'''
            SELECT * 
            FROM users 
            WHERE {' AND '.join(conditions)} 
            ORDER BY username ASC 
            LIMIT {req.num} OFFSET {req.offset};
            ''')
            for r in cur:
                res.append(User(*r))
        return res

    def insert_user(self, usr: User) -> User:
        self._logger.debug(f'[persistence] insert_user: usr={usr}')
        with self._connector.get_conn().cursor() as cur:
            cur.execute(f'INSERT INTO users VALUES {usr.to_sql_format()};')
        return usr

    def delete_user_by_name(self, name: str) -> None:
        self._logger.debug(f'[persistence] delete_user_by_name: name={name}')
        with self._connector.get_conn().cursor() as cur:
            cur.execute(f'DELETE FROM users WHERE username=\'{name}\';')

    def update_user(self, req: UserUpdateRequest) -> User:
        self._logger.error(f'[persistence] update_user: req={req}')
        fields_to_update = []
        if req.email:
            fields_to_update.append(f'email=\'{req.email}\'')
        if req.role:
            fields_to_update.append(f'role=\'{req.role.name}\'')
        if req.icon_id:
            fields_to_update.append(f'icon_id={req.icon_id}')
        if req.new_password:
            fields_to_update.append(f'password_hash=\'{req.new_password}\'')
        if len(fields_to_update) is 0:
            return self.get_user_by_name(req.username)
        with self._connector.get_conn().cursor() as cur:
            cur.execute(f'''
            UPDATE users 
            SET {','.join(fields_to_update)} 
            WHERE username=\'{req.username}\' 
            RETURNING *;
            ''')
            for r in cur:
                return User(*r)