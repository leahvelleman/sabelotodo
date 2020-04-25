from dataclasses import dataclass
import datetime
import re
from marshmallow import fields, validates, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sabelotodo import db
from werkzeug.security import generate_password_hash, check_password_hash

GMT = datetime.timezone(datetime.timedelta(hours=0))


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = (db.UniqueConstraint('username',
                                          name='unique_username'),)

    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String, nullable=False)
    password: str = db.Column(db.String(200), nullable=False)
    email: str = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        errors = UserSchema().validate(kwargs)
        if errors:
            raise ValidationError("Provided data does not match user schema")
        self.username = kwargs['username']
        self.email = kwargs['email']
        # Don't set password directly; do it through the method so it gets
        # hashed.
        self.set_password(kwargs['password'])

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Confirm hashed password."""
        return check_password_hash(self.password, password)


def validate_username(s):
    """ Validate username according to arbitrary but sensible guidelines:
    can't be too short or too long, can't have anything outside of the full
    range of Unicode letters and digits. """
    if len(s) < 3:
        raise ValidationError("Username %s too short." % s)
    if len(s) > 30:
        raise ValidationError("Username %s too long." % s)
    if not re.fullmatch(r"\w*", s):
        raise ValidationError("Username %s has non-alphanumeric characters." % s)


def validate_password(s):
    """ Validate password according to NIST guidelines: can't be too short,
    can't be too long, otherwise anything is permitted. """
    if len(s) < 8:
        raise ValidationError("Password too short.")
    if len(s) > 64:
        raise ValidationError("Password too long.")


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        sqla_session = db.session
        load_only = ('password',)  # Refuse to serialize a password

    username = fields.Str(validate=validate_username)
    password = fields.Str(validate=validate_password)
    email = fields.Email()


@dataclass(eq=True, order=True)  # Support equality and sorting
class Item(db.Model):
    __tablename__ = 'items'
    __table_args__ = (db.UniqueConstraint('order', 'parent_id',
                                          name='sibling_order'),)

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(256), nullable=False)
    order: int = db.Column(db.Integer, nullable=False)
    done: bool = db.Column(db.Boolean, nullable=False)
    description: str = db.Column(db.String)
    start_date: datetime = db.Column(db.DateTime)
    end_date: datetime = db.Column(db.DateTime)
    due_date: datetime = db.Column(db.DateTime)
    parent_id: int = db.Column(db.Integer, db.ForeignKey('items.id'))

    def __init__(self, **kwargs):
        errors = ItemSchema().validate(kwargs)
        if errors:
            raise ValidationError("Provided data does not match user schema")
        for k in kwargs:
            setattr(self, k, kwargs[k])


class ItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        include_fk = True
        sqla_session = db.session

    # Override these fields so we can tell Marshmallow more about
    # time format and time zone. `NaiveDateTime` means we're not
    # attempting to store a time zone. The `format` argument means
    # we expect JSON strings in the format Flask emits by default.
    # The `timezone` argument prevents off-by-a-few-hours
    # errors we were otherwise getting -- I'm unclear on why it needs
    # to be specified, but empirically it works. (lbv)
    start_date = fields.NaiveDateTime(format="rfc", timezone=GMT,
                                      allow_none=True)
    due_date = fields.NaiveDateTime(format="rfc", timezone=GMT,
                                    allow_none=True)
    end_date = fields.NaiveDateTime(format="rfc", timezone=GMT,
                                    allow_none=True)
