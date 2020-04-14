from flask import current_app
from sqlalchemy import asc, desc

from app import db
from app.businesses.models import Business, Category, Tag, User

CONTAINS = '%{}%'


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

    def get(self, id, description="Object doesnt exist", strict=False):
        entity = self.query.get_or_404(id, description=description)
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

    def exist(self, id=None):
        if id:
            return self.get(id)
        else:
            False

    @classmethod
    def _update_fields(cls, db_entity, **kwargs):
        for key, value in kwargs.items():
            setattr(db_entity, key, value)

    def _delete(self, id_):
        db_entity = self.get(id_)
        if not db_entity:
            raise KeyError("DB Object not found.")
        self.session.delete(db_entity)
        self.session.commit()
        return True


class BusinessRepository(BaseRepository):
    model = Business

    def save(self, entity):
        super(BusinessRepository, self).save(entity)
        return entity

    def filter(self, querySearch=None, accepted_at=None, status=None, order=None, order_by=None, **kwargs):
        query = self.query

        if querySearch:
            querySearch = CONTAINS.format(querySearch)
            query = query.filter(Business.name.ilike(querySearch) | Business.description.ilike(querySearch))

        if accepted_at:
            query = query.filter(Business.accepted_at == accepted_at)

        if status:
            for s in status:
                query = query.filter(Business.status == s)

        if order_by:
            order = asc if order == "ASC" else desc
            if order_by == "name":
                query = query.order_by(order(Business.name))

        return query


class CategoryRepository(BaseRepository):
    model = Category

    def save(self, entity):
        super(CategoryRepository, self).save(entity)
        return entity

    def filter(self, *args, **kwargs):
        query = super(CategoryRepository, self).filter(**kwargs)

        return query

    def delete(self, id_):

        category = self.get(id_, description="Category doesnt exist")

        if category is None or len(category.businesses) > 0:
            return False

        return self._delete(id_)


class TagRepository(BaseRepository):
    model = Tag

    def save(self, entity):
        super(TagRepository, self).save(entity)
        return entity

    def filter(self, *args, **kwargs):
        query = super(TagRepository, self).filter(**kwargs)

        return query

    def delete(self, id_):
        category = self.get(id_, description="Tag doesnt exist")

        if category is None:
            return False

        return self._delete(id_)


class UserRepository(BaseRepository):
    model = User

    def save(self, entity):
        super(UserRepository, self).save(entity)
        return entity

    def filter(self, *args, **kwargs):
        query = super(UserRepository, self).filter(**kwargs)

        return query

    def delete(self, id_):
        user = self.get(id_)

        if user is None:
            return False

        return self._delete(id_)
