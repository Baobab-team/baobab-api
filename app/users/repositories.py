from app.common.repositories import BaseRepository
from app.users.models import User


class UserRepository(BaseRepository):
    model = User

    def save(self, entity):
        super(UserRepository, self).save(entity)
        return entity

    def exist(self, email):
        entity = self.filter(email=email).first()
        if entity:
            return True
        return False

    def filter(self, *args, **kwargs):
        query = super(UserRepository, self).filter(**kwargs)

        return query

    def delete(self, id_):

        user = self.get(id_)

        if user is None :
            return False

        return self._delete(id_)
