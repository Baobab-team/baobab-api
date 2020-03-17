from flask_restful import Resource, abort
from flask_restful.reqparse import Argument

from app.utils.decorators import parse_with, marshal_with, parse_request
from .models import Tag
from .repositories import BusinessRepository, CategoryRepository, TagRepository
from .schemas import BusinessCreateSchema, CategorySchema, CategoryCreateSchema, CategoryUpdateSchema, BusinessSchema, \
    BusinessUpdateSchema, TagSchema, TagSchemaCreateOrUpdate, TagListSchema


class BusinessCollection(Resource):
    """
    Show a list of businesses and lets you add it
    """

    def __init__(self, repository_factory=BusinessRepository):
        super(BusinessCollection, self).__init__()
        self.repository = repository_factory()

    @parse_request(
        Argument("querySearch", type=str, store_missing=False),
        Argument("status", type=str, store_missing=False),
        Argument("accepted_at", type=str, store_missing=False),
    )
    @marshal_with(BusinessSchema, many=True, success_code=200)
    def get(self, *args, **kwargs):
        businesesses = self.repository.filter(*args, **kwargs).all()
        return businesesses

    @parse_with(BusinessCreateSchema(), arg_name="entity")
    @marshal_with(BusinessSchema, success_code=201)
    def post(self, entity, **kwargs):
        if self.repository.exist(entity.name):
            abort(400, message="Business already exist")

        return self.repository.save(entity)


class BusinessScalar(Resource):

    def __init__(self, repository_factory=BusinessRepository):
        super(BusinessScalar, self).__init__()
        self.repository = repository_factory()

    @parse_with(BusinessUpdateSchema(), arg_name="entity")
    @marshal_with(BusinessSchema)
    def put(self, id, entity):
        return self.repository.update(id, **entity)

    @marshal_with(BusinessSchema)
    def get(self, id):
        return self.repository.query.filter_by(id=id).first_or_404(description='Business doesnt exist')


class BusinessTagCollection(Resource):

    def __init__(self, repository_factory=BusinessRepository):
        super(BusinessTagCollection, self).__init__()
        self.repository = repository_factory()

    @marshal_with(TagSchema, many=True)
    def get(self, id):
        business = self.repository.get(id, description="Business doesnt exist")
        return business.tags

    @parse_with(TagSchema(), many=True, arg_name="tags")
    @marshal_with(TagSchema, many=True, success_code=201)
    def post(self, id, tags, **kwargs):
        business = self.repository.get(id, description='Business doesnt exist')

        for tag in tags:
            tag.addBusinessTag(business)

        self.repository.save(business)
        return business.tags


class BusinessTagScalar(Resource):

    def __init__(self, repository_factory=BusinessRepository):
        super(BusinessTagScalar, self).__init__()
        self.repository = repository_factory()

    def delete(self, id, tag_id, **kwargs):
        business = self.repository.get(id, description='Business doesnt exist')
        tag = Tag.query.get(tag_id)
        tag.removeBusinessTag(business)

        self.repository.save(business)

        return None,204

class CategoryScalar(Resource):

    def __init__(self, repository_factory=CategoryRepository):
        super(CategoryScalar, self).__init__()
        self.repository = repository_factory()

    @parse_with(CategoryUpdateSchema(), arg_name="entity")
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

    @parse_with(CategoryCreateSchema(), arg_name="entity")
    @marshal_with(CategorySchema, success_code=201)
    def post(self, entity, **kwargs):
        if self.repository.exist(entity.name):
            abort(400, message="Category already exist")

        return self.repository.save(entity)


class TagScalar(Resource):

    def __init__(self, repository_factory=TagRepository):
        super(TagScalar, self).__init__()
        self.repository = repository_factory()

    @parse_with(TagSchemaCreateOrUpdate(), arg_name="entity")
    @marshal_with(TagSchema)
    def put(self, id, entity, **kwargs):
        return self.repository.update(id, **entity)

    def delete(self, id):

        # return proper status code
        if self.repository.delete(id):
            return None, 204
        else:
            return {"message": "Tag doesnt exist"}, 404

    @marshal_with(TagSchema)
    def get(self, id):
        return self.repository.query.filter_by(id=id).first_or_404(description='Tag doesnt exist')


class TagCollection(Resource):

    def __init__(self, repository_factory=TagRepository):
        super(TagCollection, self).__init__()
        self.repository = repository_factory()

    @marshal_with(TagSchema, many=True, success_code=200)
    def get(self):
        return self.repository.query.all()

    @parse_with(TagSchema(), arg_name="entity")
    @marshal_with(TagSchema, success_code=201)
    def post(self, entity, **kwargs):
        if self.repository.exist(entity.name):
            abort(400, message="Tag already exist")

        return self.repository.save(entity)
