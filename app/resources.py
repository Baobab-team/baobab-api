from flask import jsonify
from flask_restful import Resource, reqparse
from flask_restful.representations import json

from app import db
from app.models import Business, BusinessSchema

business_schema = BusinessSchema(many=True)

parser = reqparse.RequestParser()
parser.add_argument("business")


class BusinessResource(Resource):
    def get(self):
        list = Business.query.all()

        data = business_schema.dump(list).data
        return jsonify({"businesses": data})

    def post(self):
        args = parser.parse_args()
        business = Business(args["business"])
        db.session.add(business)
        db.session.commit()

    def put(self, id):
        args = parser.parse_args()
        business = Business.query.filter_by(id=id).first()
        business.update(dict(args["business"]))
        db.session.commit()

