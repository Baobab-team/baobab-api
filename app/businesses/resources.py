import os
import time as ttime

import textdistance
import werkzeug
from flask import jsonify, current_app
from flask_restful import Resource, abort
from flask_restful.reqparse import Argument
from sqlalchemy.exc import IntegrityError
from werkzeug.datastructures import FileStorage

from app.utils.decorators import parse_with, marshal_with, parse_request
from .data import process_file
from .exceptions import EntityNotFoundException, BaseException, ConflictException
from .models import Tag
from .repositories import BusinessRepository, CategoryRepository, TagRepository, BusinessUploadRepository
from .schemas import BusinessCreateSchema, CategorySchema, CategoryUpdateSchema, BusinessSchema, \
    BusinessUpdateSchema, TagSchema, TagSchemaCreateOrUpdate, BusinessUploadSchema
from ..consts import BUSINESS_PER_PAGE


class BusinessCollection(Resource):
    """
    Show a list of businesses and lets you add it
    """

    def __init__(self, repository_factory=BusinessRepository):
        super(BusinessCollection, self).__init__()
        self.repository = repository_factory()

    @parse_request(
        Argument("querySearch", type=str, store_missing=False),
        Argument("status", type=str, store_missing=False, action="append"),
        Argument("accepted_at", type=str, store_missing=False),
        Argument("order_by", type=str, choices=("name"), default='name'),
        Argument("order", type=str, choices=("ASC", "DESC"), default="ASC"),
        Argument("page", type=int, default=1),
        Argument("businessPerPage", type=int, default=BUSINESS_PER_PAGE),
        Argument("exclude_deleted", type=bool, default=True),
    )
    @marshal_with(BusinessSchema, many=True, success_code=200)
    def get(self, page, exclude_deleted, businessPerPage, status=None, querySearch=None, accepted_at=None, order=None,
            order_by=None,
            **kwargs):
        return self.repository.filter(
            querySearch=querySearch, accepted_at=accepted_at, status=status, order=order,
            order_by=order_by, exclude_deleted=exclude_deleted, **kwargs
        ).paginate(page, businessPerPage, False).items

    @parse_with(BusinessCreateSchema(), arg_name="entity")
    @marshal_with(BusinessSchema, success_code=201)
    def post(self, entity, **kwargs):
        try:
            return self.repository.save(entity)
        except (EntityNotFoundException, Exception):
            raise


class BusinessScalar(Resource):

    def __init__(self, repository_factory=BusinessRepository):
        super(BusinessScalar, self).__init__()
        self.repository = repository_factory()

    @parse_with(BusinessUpdateSchema(), arg_name="entity")
    @marshal_with(BusinessSchema)
    def put(self, id, entity):
        return self.repository.update(id, **entity)

    @parse_request(
        Argument("exclude_deleted", type=bool, default=True),
    )
    @marshal_with(BusinessSchema)
    def get(self, id, exclude_deleted):
        return self.repository.filter(id=id, exclude_deleted=exclude_deleted).first_or_404(
            description='Business doesnt exist')

    def delete(self, id):
        self.repository.delete(id=id)
        return None, 204


class BusinessSearchAutoCompleteCollection(Resource):

    def __init__(self, repository_factory=BusinessRepository):
        super(BusinessSearchAutoCompleteCollection, self).__init__()
        self.repository = repository_factory()

    @parse_request(
        Argument("querySearch", type=str, store_missing=False),
        Argument("limit", type=str, default=10),
        Argument("distance", type=float, default=.35),
        Argument("status", type=str, store_missing=False, action="append"),
        Argument("accepted_at", type=str, store_missing=False),
        Argument("order_by", type=str, choices=("name"), default='name'),
        Argument("order", type=str, choices=("ASC", "DESC"), default="ASC"),
        Argument("exclude_deleted", type=bool, default=True),
    )
    def get(self, limit, distance, exclude_deleted, status=None, querySearch=None, accepted_at=None, order=None,
            order_by=None, **kwargs):
        full_business_list = self.repository.filter(
            accepted_at=accepted_at, status=status, order=order,
            order_by=order_by, exclude_deleted=exclude_deleted, **kwargs
        ).all()
        search_matching_business_list = self.repository.filter(
            querySearch=querySearch, accepted_at=accepted_at, status=status, order=order,
            order_by=order_by, exclude_deleted=exclude_deleted, **kwargs
        )
        if querySearch is None:
            response = jsonify({"message": "Missing query search parameter"})
            response.status_code = 400
            return response

        matching_words = set([])
        for b in full_business_list:
            keyword = querySearch.lower()
            matching_name = textdistance.levenshtein.normalized_distance(b.name.lower(), keyword) < distance

            if matching_name:
                matching_words.add(b.name)

            for tag in b.tags:
                matching_tag = textdistance.levenshtein.normalized_distance(tag.name.lower(), keyword) < distance
                if matching_tag:
                    matching_words.add(tag.name)

        for b in search_matching_business_list:
            matching_words.add(b.name)

        matching_words = list(matching_words)[0:limit]
        response = jsonify(matching_words)
        response.status_code = 200
        return response



class BusinessUploadCollection(Resource):

    def __init__(self, business_repository_factory=BusinessRepository, business_upload_repository=BusinessUploadRepository):
        super(BusinessUploadCollection, self).__init__()
        self.business_repository = business_repository_factory()
        self.business_upload_repository = business_upload_repository()

    @marshal_with(BusinessUploadSchema, many=True)
    def get(self):
        return self.business_upload_repository.query.all()

    @parse_request(
        Argument("file", type=werkzeug.datastructures.FileStorage, location='files'),
    )
    @marshal_with(BusinessUploadSchema, success_code=200)
    def post(self, file):
        filename = os.path.join(current_app.config["UPLOAD_FOLDER"],
                                "business-{}.csv".format(ttime.strftime("%Y-%m-%d_%H-%M-%S")))

        try:
            if file is None or file.filename == '' :
                raise BaseException(message="No file uploaded")

            current_app.logger.info(file.filename)
            file.save(filename)
            upload = process_file(filename)  # TODO move to a background job or something
            current_app.logger.info("File uploaded!")

            return upload
        except Exception as e:
            current_app.logger.error(str(e))
            abort(400, message=f"An error occurred during the process: {str(e.args[0])}")


class BusinessUploadScalar(Resource):

    def __init__(self, repository=BusinessUploadRepository):
        super(BusinessUploadScalar, self).__init__()
        self.repository = repository()

    @marshal_with(BusinessUploadSchema)
    def get(self, id):
        return self.repository.get(id)


class BusinessTagCollection(Resource):

    def __init__(self, repository_factory=BusinessRepository):
        super(BusinessTagCollection, self).__init__()
        self.repository = repository_factory()

    @parse_request(
        Argument("exclude_deleted", type=bool, default=True),
    )
    @marshal_with(TagSchema, many=True)
    def get(self, id, exclude_deleted):
        business = self.repository.filter(id=id, exclude_delete=exclude_deleted).first_or_404(
            description='Business doesnt exist')
        return business.tags

    @parse_with(TagSchema(), many=True, arg_name="tags")
    @marshal_with(TagSchema, many=True, success_code=201)
    def post(self, id, tags, **kwargs):
        business = self.repository.get(id)

        for tag in tags:
            tag.addBusinessTag(business)

        self.repository.save(business)
        return business.tags


class BusinessTagScalar(Resource):

    def __init__(self, repository_factory=BusinessRepository):
        super(BusinessTagScalar, self).__init__()
        self.repository = repository_factory()

    def delete(self, id, tag_id, **kwargs):
        business = self.repository.get(id)
        tag = Tag.query.get(tag_id)
        tag.removeBusinessTag(business)

        self.repository.save(business)

        return None, 204


class CategoryScalar(Resource):

    def __init__(self, repository_factory=CategoryRepository):
        super(CategoryScalar, self).__init__()
        self.repository = repository_factory()

    @parse_with(CategoryUpdateSchema(), arg_name="entity")
    @marshal_with(CategorySchema)
    def put(self, id, entity, **kwargs):
        return self.repository.update(id, **entity)

    def delete(self, id):
        try:
            self.repository.delete(id)
            return None, 204
        except EntityNotFoundException:
            raise

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

    @parse_with(CategorySchema(), arg_name="entity")
    @marshal_with(CategorySchema, success_code=201)
    def post(self, entity, **kwargs):
        try:
            return self.repository.save(entity)
        except (ConflictException, BaseException):
            raise

class TagScalar(Resource):

    def __init__(self, repository_factory=TagRepository):
        super(TagScalar, self).__init__()
        self.repository = repository_factory()

    @parse_with(TagSchemaCreateOrUpdate(), arg_name="entity")
    @marshal_with(TagSchema)
    def put(self, id, entity, **kwargs):
        return self.repository.update(id, **entity)

    def delete(self, id):

        try:
            self.repository.delete(id)
            return None, 204
        except EntityNotFoundException:
            raise

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
        try:
            return self.repository.save(entity)
        except ConflictException:
            raise
