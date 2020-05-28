def populate(_db, cls, data):
    objs = [cls(**d) for d in data]
    _db.session.add_all(objs)
    _db.session.commit()
    return objs
