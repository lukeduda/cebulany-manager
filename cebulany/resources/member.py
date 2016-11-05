from flask_restful import Resource, fields, marshal_with
from flask_restful.reqparse import RequestParser
from sqlalchemy import or_, func as sql_func
from datetime import datetime

from cebulany.models import db, Member

member_parser = RequestParser()
member_parser.add_argument('name')
member_parser.add_argument('join_date')
member_parser.add_argument('is_active', type=bool)

query_parser = RequestParser()
query_parser.add_argument('q')


member_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'join_date': fields.DateTime(dt_format='iso8601'),
    'is_active': fields.Boolean,
}


class MemberListResource(Resource):

    @marshal_with(member_fields)
    def get(self):
        args = query_parser.parse_args()
        query = Member.query.order_by(Member.name)
        query_arg = args['q']
        if query_arg:
            args = query_arg.split()
            query = query.filter(*[
                Member.name.ilike('%%%s%%' % arg.replace('%',r'\%'))
                for arg in args
            ])
        return query.limit(5).all()

    @marshal_with(member_fields)
    def post(self):
        args = member_parse.parse_args()
        member = Member(**parse.args())
        db.session.add(member)
        db.session.commit()
        return member, 201


class MemberResource(Resource):

    @marshal_with(member_fields)
    def get(self, id):
        return Member.query.get(id)

    def delete(self, id):
        db.session.delete(Member.query.get(id))
        return 204

