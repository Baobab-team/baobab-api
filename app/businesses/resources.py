from flask_restful import Resource, abort

from app.utils.decorators import parse_with, marshal_with
from .models import Business
from .repositories import BusinessRepository, CategoryRepository
from .schemas import BusinessCreateSchema, CategorySchema, CategoryCreateSchema, CategoryUpdateSchema


class BaseResource(Resource):

    def __init__(self):
        super(BaseResource, self).__init__()


class BusinessCollection(Resource):
    """
    Show a list of businesses and lets you add it
    """

    def __init__(self, repository_factory=BusinessRepository):
        super(BusinessCollection, self).__init__(api=None)
        self.repository = repository_factory()

    def get(self):
        list = Business.query.all()
        business_schema = BusinessCreateSchema(many=True)
        data = business_schema.dump(list).data
        return data, 200

    @parse_with(BusinessCreateSchema(strict=True), arg_name="entity")
    def post(self, entity, **kwargs):
        business = self.repository.save(entity)
        return {"message": "business created"}, 201


class BusinessScalar(Resource):

    def __init__(self, repository_factory=BusinessRepository):
        super(BusinessScalar, self).__init__()
        self.repository = repository_factory()

    @parse_with(BusinessCreateSchema(strict=True), arg_name="entity")
    def put(self, id, entity):
        return self.repository.update(id, **entity)

    def delete(self, id_):
        # return proper status code
        self.repository.delete(id_)
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
        """

        :param id:
        :return response:
        """
        # return proper status code
        if self.repository.delete(id):
            return None, 204
        else:
            return {"message": "Category doesnt exist or os related to to businesses"}, 404

    @marshal_with(CategorySchema)
    def get(self, id):
        return self.repository.query.filter_by(id=id).first_or_404(description='Category doesnt exist')


class CategoriesCollection(Resource):

    def __init__(self, repository_factory=CategoryRepository):
        super(CategoriesCollection, self).__init__()
        self.repository = repository_factory()

    @marshal_with(CategorySchema, many=True, success_code=201)
    def get(self):
        return self.repository.query.all()

    @parse_with(CategoryCreateSchema(strict=True), arg_name="entity")
    @marshal_with(CategorySchema, success_code=201)
    def post(self, entity, **kwargs):
        if self.repository.exist(entity.name):
            abort(400, message="Category already exist")

        return self.repository.save(entity)
