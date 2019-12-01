from app.businesses.models import Business, Category
from app.common.repositories import BaseRepository

CONTAINS = '%{}%'


class BusinessRepository(BaseRepository):
    model = Business

    def save(self, entity):
        super(BusinessRepository, self).save(entity)
        return entity

    def filter(self, *args, **kwargs):
        query = self.query
        if "name" in kwargs:
            name = CONTAINS.format(kwargs.get("name"))
            query = query.filter(Business.name.like(name))

        if "description" in kwargs:
            description = CONTAINS.format(kwargs.get("description"))
            query = query.filter(Business.description.like(description))

        if "accepted" in kwargs:
            query = query.filter(Business.accepted == kwargs.get("accepted"))

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
