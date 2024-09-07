# mm-store/app/api/routes.py
from flask import request
from flask_restx import Resource, fields
from ..models import db, Store
from ..schemas import StoreSchema
from sqlalchemy import or_

def init_routes(api):
    store_schema = StoreSchema()

    # Data store_model for a store
    store_model = api.model('Store', {
        'id': fields.Integer(readOnly=True, description='The unique identifier of a store'),
        'ownerid': fields.Integer(required=True, description='The identifier of the store owner'),
        'addressid': fields.Integer(required=True, description='The identifier of the store address'),
        'cnpj': fields.String(required=True, description='CNPJ of the store'),
        'name': fields.String(required=True, description='Store commercial name'),
        'imageurl': fields.String(required=False, description='URL of the store image')
    })

    # Define resources and routes
    class StoreList(Resource):
        @api.marshal_list_with(store_model)
        def get(self):
            """List all stores or search by query string"""
            query = request.args.get('q')
            if query:
                search_filter = f"%{query.lower()}%"
                stores = Store.query.filter(
                    or_(
                        db.func.lower(Store.name).ilike(search_filter),
                        db.func.lower(Store.cnpj).ilike(search_filter)
                    )
                ).all()
            else:
                stores = Store.query.all()
            return stores

        @api.expect(store_model)
        @api.marshal_with(store_model, code=201)
        def post(self):
            """Create a new store"""
            data = request.json
            store = Store(**data)
            db.session.add(store)
            db.session.commit()
            return store, 201

    class StoreDetail(Resource):
        @api.marshal_with(store_model)
        def get(self, id):
            """Fetch a store given its identifier"""
            store = Store.query.get_or_404(id)
            return store

        @api.expect(store_model)
        @api.marshal_with(store_model)
        def put(self, id):
            """Update a store"""
            store = Store.query.get_or_404(id)
            data = request.json
            for key, value in data.items():
                setattr(store, key, value)
            db.session.commit()
            return store

        @api.response(204, 'Store deleted')
        def delete(self, id):
            """Delete a store"""
            store = Store.query.get_or_404(id)
            db.session.delete(store)
            db.session.commit()
            return '', 204

    # Register routes
    api.add_resource(StoreList, '/mm-store')
    api.add_resource(StoreDetail, '/mm-store/<int:id>')
