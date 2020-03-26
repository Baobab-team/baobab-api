from sqlalchemy import asc, desc

from app.businesses.models import Business, Category, Tag
from app.common.repositories import BaseRepository

CONTAINS = '%{}%'


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

    def exist(self, name):
        entity = self.query.filter_by(name=name).first()
        if entity:
            return True
        return False


class CategoryRepository(BaseRepository):
    model = Category

    def save(self, entity):
        super(CategoryRepository, self).save(entity)
        return entity

    def exist(self, name):
        entity = self.query.filter_by(name=name).first()
        if entity:
            return True
        return False

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

    def exist(self, name):
        entity = self.query.filter_by(name=name).first()
        if entity:
            return True
        return False

    def filter(self, *args, **kwargs):
        query = super(TagRepository, self).filter(**kwargs)

        return query

    def delete(self, id_):
        category = self.get(id_, description="Tag doesnt exist")

        if category is None:
            return False

        return self._delete(id_)
