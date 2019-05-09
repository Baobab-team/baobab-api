from flask import current_app

from app import db


class BaseRepository(object):
    model = None
    _session = None

    def __init__(self):
        self._session = db.session

    @property
    def session(self):
        return self._session or current_app.session()

    @property
    def query(self):
        assert self.model, "A model is required to use the query property."
        return self.session.query(self.model)

    def get(self, id_, strict=False):
        entity = self.query.get(id_)
        if strict and not entity:
            raise KeyError("DB Object not found.")
        return entity

    def filter(self, **kwargs):
        query = self.query.filter_by(**kwargs)
        return query

    def save(self, entity):
        self.session.add(entity)
        self.session.commit()
        return entity

    def update(self, id_, **kwargs):
        db_entity = self.get(id_)
        if not db_entity:
            raise KeyError("DB Object not found.")
        self._update_fields(db_entity, **kwargs)
        self.session.commit()
        return db_entity

    @classmethod
    def _update_fields(cls, db_entity, **kwargs):
        for key, value in kwargs.items():
            setattr(db_entity, key, value)

    def delete(self, id_):
        db_entity = self.get(id_)
        if not db_entity:
            raise KeyError("DB Object not found.")
        self.session.delete(db_entity)
        self.session.commit()
        return True
