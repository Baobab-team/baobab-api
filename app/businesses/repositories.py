from flask import current_app
from sqlalchemy import asc, desc
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.businesses.models import Business, Category, Tag, BusinessUpload

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

    def get(self, id, error_message="Object doesnt exist", strict=False):
        entity = self.query.get_or_404(id, description=error_message)
        if strict and not entity:
            raise KeyError("DB Object not found.")
        return entity

    def filter(self, **kwargs):
        query = self.query.filter_by(**kwargs)
        return query

    def save(self, entity):
        self.session.add(entity)
        try:
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise
        return entity

    def save_many(self, entities):
        self.session.add_all(entities)
        self.session.commit()
        return entities


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
        entity = self.save_tags(entity)
        super(BusinessRepository, self).save(entity)
        return entity

    def save_tags(self, entity):
        tag_repository = TagRepository()
        existing_tag = {t.name: t for t in tag_repository.query.all()}
        tag_to_be_add = []
        for t in entity.tags:
            if t.name in existing_tag:
                tag_to_be_add.append(existing_tag[t.name])
            else:
                tag_to_be_add.append(t)
        entity.tags = tag_to_be_add
        return entity

    def filter(self, id=None, querySearch=None, accepted_at=None, status=None, order=None, order_by=None,
               exclude_deleted=None,
               **kwargs):
        query = self.query

        if exclude_deleted:
            query = query.filter(Business.deleted_at.is_(None))

        if id:
            return query.filter(Business.id == id)

        if querySearch:
            querySearch = CONTAINS.format(querySearch)
            query = query.filter(Business.name.ilike(querySearch))

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

    def delete(self, id, error_message):
        business = self.get(id=id, error_message=error_message)
        business.delete()
        self.save(business)


class CategoryRepository(BaseRepository):
    model = Category

    def save(self, entity):
        super(CategoryRepository, self).save(entity)
        return entity

    def filter(self, *args, **kwargs):
        query = super(CategoryRepository, self).filter(**kwargs)

        return query

    def delete(self, id_):
        category = self.get(id_, error_message="Category doesnt exist")

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
        category = self.get(id_, error_message="Tag doesnt exist")

        if category is None:
            return False

        return self._delete(id_)


class BusinessUploadLogRepository(BaseRepository):
    model = BusinessUpload
