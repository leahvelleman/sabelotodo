from dataclasses import dataclass
from sabelotodo import db


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
    start_date: str = db.Column(db.DateTime)
    end_date: str = db.Column(db.DateTime)
    due_date: str = db.Column(db.DateTime)
    parent_id: int = db.Column(db.Integer, db.ForeignKey('items.id'))
