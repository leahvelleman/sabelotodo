from sabelotodo import db



class Item(db.Model):
    __table_args__ = (db.UniqueConstraint('order', 'parent_id', name='sibling_order'),)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    done = db.Column(db.Boolean, nullable=False)
    description = db.Column(db.String)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime)
    parent_id = db.Column(db.Integer, db.ForeignKey('item.id'))

    def __init__(self, name, order, done=False, description=None, 
            start_date=None, end_date=None, due_date=None, 
            parent_id=None):
        self.name = name
        self.order = order
        self.done = done
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.due_date = due_date
        self.parent_id = parent_id

    def __repr__(self):
        return '<Item {}>'.format(self.name)
