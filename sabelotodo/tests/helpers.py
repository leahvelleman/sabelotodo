def populate(_db, schema, data):
    objs = schema.load(data)
    _db.session.add_all(objs)
    _db.session.commit()
    return objs
