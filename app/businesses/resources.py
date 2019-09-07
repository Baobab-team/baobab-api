from flask_restful import Resource, abort

from app.utils.decorators import parse_with, marshal_with
from .repositories import BusinessRepository, CategoryRepository, UserRepository
from .schemas import BusinessCreateSchema, CategorySchema, CategoryCreateSchema, CategoryUpdateSchema, BusinessSchema, \
    BusinessUpdateSchema, UserUpdateSchema, UserSchema, UserCreateSchema


class BusinessCollection(Resource):
    """
    Show a list of businesses and lets you add it
    """

    def __init__(self, repository_factory=BusinessRepository):
        super(BusinessCollection, self).__init__()
        self.repository = repository_factory()

    @marshal_with(BusinessSchema, many=True, success_code=200)
    def get(self):
        return self.repository.query.all()

    @parse_with(BusinessCreateSchema(strict=True), arg_name="entity")
    @marshal_with(BusinessSchema, success_code=201)
    def post(self, entity, **kwargs):
        if self.repository.exist(entity.name):
            abort(400, message="Business already exist")

        return self.repository.save(entity)


class BusinessScalar(Resource):

    def __init__(self, repository_factory=BusinessRepository):
        super(BusinessScalar, self).__init__()
        self.repository = repository_factory()

    @parse_with(BusinessUpdateSchema(strict=True), arg_name="entity")
    @marshal_with(BusinessSchema)
    def put(self, id, entity):
        return self.repository.update(id, **entity)

    @marshal_with(BusinessSchema)
    def get(self, id):
        return self.repository.query.filter_by(id=id).first_or_404(description='Business doesnt exist')

    def delete(self, id):
        # return proper status code
        self.repository.delete(id)
        return None, 204


class CategoryScalar(Resource):

    def __init__(self, repository_factory=CategoryRepository):
        super(CategoryScalar, self).__init__()
        self.repository = repository_factory()

    @parse_with(CategoryUpdateSchema(strict=True), arg_name="entity")
    @marshal_with(CategorySchema)
    def put(self, id, entity, **kwargs):
        return self.repository.update(id, **entity)

    def delete(self, id):

        # return proper status code
        if self.repository.delete(id):
            return None, 204
        else:
            return {"message": "Category doesnt exist"}, 404

    @marshal_with(CategorySchema)
    def get(self, id):
        return self.repository.query.filter_by(id=id).first_or_404(description='Category doesnt exist')


class CategoriesCollection(Resource):

    def __init__(self, repository_factory=CategoryRepository):
        super(CategoriesCollection, self).__init__()
        self.repository = repository_factory()

    @marshal_with(CategorySchema, many=True, success_code=200)
    def get(self):
        return self.repository.query.all()

    @parse_with(CategoryCreateSchema(strict=True), arg_name="entity")
    @marshal_with(CategorySchema, success_code=201)
    def post(self, entity, **kwargs):
        if self.repository.exist(entity.name):
            abort(400, message="Category already exist")

        return self.repository.save(entity)


class UserScalar(Resource):
    """
    Show user and lets you remove/add/update it
    """
    def __init__(self, repository_factory=UserRepository):
        super(UserScalar, self).__init__()
        self.repository = repository_factory()

    @parse_with(UserUpdateSchema(strict=True), arg_name="entity")
    @marshal_with(UserSchema)
    def put(self, id, entity):
        return self.repository.update(id, **entity)

    @marshal_with(UserSchema)
    def get(self, id):
        return self.repository.query.filter_by(id=id).first_or_404(description='User doesnt exist')

    def delete(self, id):
        # return proper status code
        self.repository.delete(id)
        return None, 204


class UserCollection(Resource):

    def __init__(self, repository_factory=UserRepository):
        super(UserCollection, self).__init__()
        self.repository = repository_factory()

    @marshal_with(UserSchema, many=True, success_code=200)
    def get(self):
        return self.repository.query.all()

    @parse_with(UserCreateSchema(strict=True), arg_name="entity")
    @marshal_with(UserSchema, success_code=201)
    def post(self, entity, **kwargs):
        if self.repository.exist(entity.name):
            abort(400, message="User already exist")

        return self.repository.save(entity)

    def delete(self, id):
        # return proper status code
        self.repository.delete(id) # TODO Change for deactivate
        return None, 204