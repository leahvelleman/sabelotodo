from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sabelotodo.database import Base

class Item(Base):

    # A to-do item. Items can form trees, with each storing the id of its
    # parent if it has one. The order field represents the order among
    # siblings, and in any set of siblings, order numbers must be unique.

    __tablename__ = 'items'
    __table_args__ = (UniqueConstraint('order','parent_id',name='sibling_order'))
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    order = Column(Integer, unique=True)
    done = Column(Boolean)
    description = Column(String)
    parent_id = Column(Integer, ForeignKey('items.id'))

    def __init__(self, name, order=None, 
            done=False, description="", parent_id=None):
        self.name = name
        self.order = order
        self.done = done
        self.description = description
        self.parent_id = parent_id

    def __repr__(self):
        return '<Item %r>' % (self.name)
