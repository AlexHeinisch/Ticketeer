from marshmallow import Schema, fields, pre_dump, validate, RAISE, post_load
from marshmallow_enum import EnumField
from .models import Status, Ticket, TicketSearchRequest, TicketUpdateRequest, UserRole, User, LoginRequest, UserSearchRequest, UserUpdateRequest

### AUTH ###

class LoginRequestSchema(Schema):
    username = fields.Str(
        validate=validate.Length(min=1,max=20),
        required=True
    )
    password = fields.Str(
        validate=validate.Length(min=1,max=20),
        required=True
    )
    @post_load
    def make(self, data, **kwargs):
        return LoginRequest(**data)

    class Meta:
        unknown = RAISE
        ordered = True

### TAGS ###

class TagSchema(Schema):
    id = fields.Int(
        validate=validate.Range(min=0),
        required=True
    )
    name = fields.Str(
        validate=validate.Length(min=1,max=10),
        required=True
    )
    font_color = fields.Str(
        validate=validate.Length(min=6,max=6),
        required=False
    )
    bg_color = fields.Str(
        validate=validate.Length(min=6,max=6),
        required=False
    )

    class Meta:
        unknown = RAISE


### USER ###

class UserSchema(Schema):
    username = fields.Str(
        validate=validate.Length(min=1,max=20),
        required=True
    )
    password = fields.Str(
        validate=validate.Length(min=1, max=255),
        required=True,
        load_only=True
    )
    email = fields.Email(
        validate=validate.Length(min=1, max=40),
        required=True
    )
    icon_id = fields.Int(
        validate=validate.Range(min=0),
        required=False
    )
    role = EnumField(
        UserRole,
        required=False,
        by_value=False
    )

    @post_load
    def make(self, data, **kwargs):
        return User(**data)

    class Meta:
        unknown = RAISE
        ordered = True

class UserSearchRequestSchema(Schema):
    username = fields.Str(
        validate=validate.Length(min=1,max=20),
        required=False
    )
    email = fields.Str(
        validate=validate.Length(min=1, max=40),
        required=False
    )
    role = EnumField(
        UserRole,
        required=False,
        by_value=False
    )
    num = fields.Int(
        validate=validate.Range(min=1,max=100),
        required=False
    )
    offset = fields.Int(
        validate=validate.Range(min=0),
        required=False
    )

    @post_load
    def make(self, data, **kwargs) -> UserSearchRequest:
        if 'username' not in data:
            data['username'] = None
        if 'email' not in data:
            data['email'] = None
        if 'role' not in data:
            data['role'] = None
        return UserSearchRequest(**data)

    class Meta:
        unknown = RAISE
        ordered = True

class UserUpdateRequestSchema(Schema):
    username = fields.Str(
        validate=validate.Length(min=1,max=20),
        required=False
    )
    email = fields.Str(
        validate=validate.Length(min=1, max=40),
        required=False
    )
    old_password = fields.Str(
        validate=validate.Length(min=1,max=20),
        required=False
    )
    new_password = fields.Str(
        validate=validate.Length(min=1,max=20),
        required=False
    )
    icon_id = fields.Int(
        validate=validate.Range(min=-1),
        required=False
    )
    role = EnumField(
        UserRole,
        by_value=True,
        required=False
    )

    @post_load
    def make(self, data, **kwargs):
        if 'username' not in data:
            data['username'] = None
        if 'email' not in data:
            data['email'] = None
        if 'old_password' not in data:
            data['old_password'] = None
        if 'new_password' not in data:
            data['new_password'] = None
        if 'icon_id' not in data:
            data['icon_id'] = None
        if 'role' not in data:
            data['role'] = None
        return UserUpdateRequest(**data)

    class Meta:
        ordered = True

### TICKET ###

class TicketSchema(Schema):

    id = fields.Int(
        validate=validate.Range(min=0),
        required=True
    )
    name = fields.Str(
        validate=validate.Length(min=1,max=30),
        required=True
    )
    description = fields.Str(
        validate=validate.Length(min=1,max=2000),
        required=True
    )
    assigned_to = fields.Str(
        validate=validate.Length(min=1,max=30),
        required=False
    )
    assigned_to_changed_date = fields.DateTime(
        dump_only=True
    )
    created_by = fields.Str(
        validate=validate.Length(min=1,max=30),
        dump_only=True
    )
    creation_date = fields.DateTime(
        dump_only=True
    )
    image_ids = fields.List(
        fields.Int(
            validate=validate.Range(min=0)
        ),
        required=False
    )
    tags = fields.List(
        fields.Int(
            validate=validate.Range(min=0)
        ),
        required=False
    )
    status = EnumField(
        Status,
        by_value=True,
        required=False
    )

    @post_load
    def make(self, data, **kwargs):
        if 'id' not in data:
            data['id'] = None
        return Ticket(**data)

    class Meta:
        unknown = RAISE
        ordered = True


class TicketSearchRequestSchema(Schema):

    name = fields.Str(
        validate=validate.Length(min=1,max=30),
        required=False
    )
    description = fields.Str(
        validate=validate.Length(min=1,max=2000),
        required=False
    )
    assigned_to = fields.Str(
        validate=validate.Length(min=1,max=30),
        required=False
    )
    assigned_changed_date_before = fields.DateTime(
        required=False
    )
    assigned_changed_date_after = fields.DateTime(
        required=False
    )
    created_by = fields.Str(
        validate=validate.Length(min=1,max=30),
        required=False
    )
    creation_date_before = fields.DateTime(
        required=False
    )
    creation_date_after = fields.DateTime(
        required=False
    )
    tags = fields.List(
        fields.Int(
            validate=validate.Range(min=0)
        ),
        required=False
    )
    status = EnumField(
        Status,
        by_value=True,
        required=False
    )
    num = fields.Int(
        validate=validate.Range(min=1,max=100),
        required=False
    )
    offset = fields.Int(
        validate=validate.Range(min=0),
        required=False
    )

    @post_load
    def make(self, data, **kwargs):
        if 'name' not in data:
            data['name'] = None
        if 'description' not in data:
            data['description'] = None
        if 'assigned_to' not in data:
            data['assigned_to'] = None
        if 'assigned_changed_date_before' not in data:
            data['assigned_changed_date_before'] = None
        if 'assigned_changed_date_after' not in data:
            data['assigned_changed_date_after'] = None
        if 'created_by' not in data:
            data['created_by'] = None
        if 'creation_date_before' not in data:
            data['creation_date_before'] = None
        if 'creation_date_after' not in data:
            data['creation_date_after'] = None
        if 'tags' not in data:
            data['tags'] = None
        if 'status' not in data:
            data['status'] = None
        return TicketSearchRequest(**data)

    class Meta:
        ordered = True

class TicketUpdateRequestSchema(Schema):
    name = fields.Str(
        validate=validate.Length(min=1,max=30),
        required=False
    )
    description = fields.Str(
        validate=validate.Length(min=1,max=2000),
        required=False
    )
    assigned_to = fields.Str(
        validate=validate.Length(min=1,max=30),
        required=False
    )
    created_by = fields.Str(
        validate=validate.Length(min=1,max=30),
        required=False
    )
    tags = fields.List(
        fields.Int(
            validate=validate.Range(min=0)
        ),
        required=False
    )
    status = EnumField(
        Status,
        by_value=True,
        required=False
    )

    @post_load
    def make(self, data, **kwargs):
        if 'name' not in data:
            data['name'] = None
        if 'description' not in data:
            data['description'] = None
        if 'assigned_to' not in data:
            data['assigned_to'] = None
        if 'created_by' not in data:
            data['created_by'] = None
        if 'tags' not in data:
            data['tags'] = None
        if 'status' not in data:
            data['status'] = None
        return TicketUpdateRequest(**data)

    class Meta:
        ordered = True
