from dataclasses import dataclass
import datetime
from marshmallow import fields, post_load
from sabelotodo import db, ma

GMT = timezone=datetime.timezone(datetime.timedelta(hours=0))


@dataclass(eq=True, order=True) # Support equality and sorting for ease of
                                # testing.
class Item(db.Model):
    __tablename__ = 'items'
    __table_args__ = (db.UniqueConstraint('order', 'parent_id', name='sibling_order'),)

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(256), nullable=False)
    order: int = db.Column(db.Integer, nullable=False)
    done: bool = db.Column(db.Boolean, nullable=False)
    description: str = db.Column(db.String)
    start_date: datetime = db.Column(db.DateTime)
    end_date: datetime = db.Column(db.DateTime)
    due_date: datetime = db.Column(db.DateTime)
    parent_id: int = db.Column(db.Integer, db.ForeignKey('items.id'))

class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        include_fk = True

    # Override these fields so we can tell Marshmallow more about
    # time format and time zone. `NaiveDateTime` means we're not 
    # attempting to store a time zone. The `format` argument means
    # we expect JSON strings in the format Flask emits by default.
    # The `timezone` argument prevents off-by-a-few-hours
    # errors we were otherwise getting -- I'm unclear on why it needs
    # to be specified, but empirically it works. (lbv)
    start_date = fields.NaiveDateTime(format="rfc",timezone=GMT)
    due_date = fields.NaiveDateTime(format="rfc",timezone=GMT)
    end_date = fields.NaiveDateTime(format="rfc",timezone=GMT)

    # Instruct Marshmallow to actually instantiate an Item object when
    # it deserializes using this schema instead of just giving us
    # a dictionary we could use to instantiate one ourselves. 
    @post_load
    def make_item(self, data, **kwargs):
        return Item(**data)
