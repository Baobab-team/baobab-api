from app.businesses.models import Business, Category, Tag
from app.common.repositories import BaseRepository

CONTAINS = '%{}%'


class BusinessRepository(BaseRepository):
    model = Business

    def save(self, entity):
        super(BusinessRepository, self).save(entity)
        return entity

    def filter(self, *args, **kwargs):
        query = self.query
        if "querySearch" in kwargs:
            querySearch = CONTAINS.format(kwargs.get("querySearch"))
            query = query.filter(Business.name.ilike(querySearch) | Business.description.ilike(querySearch))

        if "accepted_at" in kwargs:
            query = query.filter(Business.accepted_at == kwargs.get("accepted_at"))

        if "status" in kwargs:
            query = query.filter(Business.status == kwargs.get("status"))

        return query

    def exist(self, name):
        entity = self.filter(name=name).first()
        if entity:
            return True
        return False


class CategoryRepository(BaseRepository):
    model = Category

    def save(self, entity):
        super(CategoryRepository, self).save(entity)
        return entity

    def exist(self, name):
        entity = self.filter(name=name).first()
        if entity:
            return True
        return False

    def filter(self, *args, **kwargs):
        query = super(CategoryRepository, self).filter(**kwargs)

        return query

    def delete(self, id_):

        category = self.get(id_)

        if category is None or len(category.businesses) > 0:
            return False

        return self._delete(id_)


class TagRepository(BaseRepository):
    model = Tag

    def save(self, entity):
        super(TagRepository, self).save(entity)
        return entity

    def exist(self, name):
        entity = self.filter(name=name).first()
        if entity:
            return True
        return False

    def filter(self, *args, **kwargs):
        query = super(TagRepository, self).filter(**kwargs)

        return query

    def delete(self, id_):
        category = self.get(id_)

        if category is None:
            return False

        return self._delete(id_)
