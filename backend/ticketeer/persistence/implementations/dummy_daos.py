from ..base_daos import TicketDao, UserDao

from ...models import User, UserUpdateRequest

class DummyTicketDao(TicketDao):

    def __init__(self) -> None:
        super().__init__()

    def get(self):
        pass

class DummyUserDao(UserDao):

    def __init__(self) -> None:
        super().__init__()
        self._storage = {}

    def get_user_by_name(self, name: str) -> User | None:
        if name in self._storage:
            return self._storage[name]
        return None

    def insert_user(self, usr: User) -> User:
        self._storage[usr.username] = usr
        return usr

    def delete_user_by_name(self, name):
        if name in self._storage:
            del self._storage[name]

    # not tested
    def get_users_by_search_req(self, req) -> list[User]:
        res = []
        for k,v in self._storage.items():
            if req.email and not req.email in v.email:
                continue
            if req.username and not req.username in v.username:
                continue
            if req.role and req.role is not v.role:
                continue
            res.append(v)
        res = sorted(res, key=lambda x: str(x.username))
        if len(res) < req.offset:
            return []
        if len(res) < req.num:
            return res
        if len(res) < req.num + req.offset:
            return res[req.offset:]
        return res[req.offset:req.offset+req.num]

    def update_user(self, req: UserUpdateRequest) -> User:
        fields_to_update = []
        usr = self.get_user_by_name(req.username)
        if req.email:
            usr.email = req.email
        if req.role:
            usr.role = req.role
        if req.icon_id:
            usr.icon_id = req.icon_id
        if req.new_password:
            usr.password = req.new_password
        self._storage[req.username] = usr
        return usr
