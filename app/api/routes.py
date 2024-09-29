# mm-store/app/api/routes.py
from flask import request
from flask_restx import Resource, fields, Namespace, reqparse
from ..models import db, Store
from ..schemas import StoreSchema
import requests
import os

def init_routes(api):
    store_ns = Namespace('stores', description='Store operations')
    api.add_namespace(store_ns, path='/mm-store')

    store_model = api.model('Store', {
        'id': fields.Integer(readOnly=True, description='The unique identifier of a store'),
        'ownerid': fields.String(description='The CPF identifier of the store owner'),
        'addressid': fields.String(description='The unique identifier of the store address'),
        'cnpj': fields.String(description='CNPJ of the store'),
        'name': fields.String(description='Store commercial name'),
        'imageurl': fields.String(description='URL of the store image')
    })

    # Define request parser for store list queries
    query_parser = reqparse.RequestParser()
    query_parser.add_argument('name', type=str, required=False, help='Filter by store name')
    query_parser.add_argument('cnpj', type=str, required=False, help='Filter by store CNPJ')
    query_parser.add_argument('addressid', type=str, required=False, help='Filter by store address ID')
    query_parser.add_argument('ownerid', type=str, required=False, help='Filter by store owner CPF')

    @store_ns.route('/')
    class StoreList(Resource):
        @store_ns.doc('list_stores')
        @store_ns.expect(query_parser)  # Use the parser for input validation and documentation
        @store_ns.marshal_list_with(store_model)
        def get(self):
            args = query_parser.parse_args()  # Parse the query parameters
            name_query = args.get('name')
            cnpj_query = args.get('cnpj')
            addressid_query = args.get('addressid')
            ownerid_query = args.get('ownerid')
            query = Store.query

            if name_query:
                query = query.filter(Store.name.ilike(f"%{name_query.lower()}%"))
            if cnpj_query:
                query = query.filter(Store.cnpj.ilike(f"%{cnpj_query.lower()}%"))
            if addressid_query:
                query = query.filter(Store.addressid == addressid_query)
            if ownerid_query:
                query = query.filter(Store.ownerid == ownerid_query)

            stores = query.all()
            return stores

        @store_ns.doc('create_store')
        @store_ns.expect(store_model)
        @store_ns.marshal_with(store_model, code=201)
        def post(self):
            data = request.json
            store = Store(
                ownerid=data['ownerid'],
                addressid=data['addressid'],
                cnpj=data['cnpj'],
                name=data['name'],
                imageurl=data.get('imageurl')
            )
            db.session.add(store)
            db.session.commit()
            return store, 201

    @store_ns.route('/<int:id>')
    class StoreDetail(Resource):
        @store_ns.doc('get_store')
        @store_ns.marshal_with(store_model)
        def get(self, id):
            store = Store.query.get_or_404(id)
            return store

        @store_ns.doc('update_store')
        @store_ns.expect(store_model)
        @store_ns.marshal_with(store_model)
        def put(self, id):
            store = Store.query.get_or_404(id)
            data = request.json
            for key, value in data.items():
                if hasattr(store, key):
                    setattr(store, key, value)
            db.session.commit()
            return store

        @store_ns.doc('delete_store')
        @store_ns.response(204, 'Store deleted')
        def delete(self, id):
            store = Store.query.get_or_404(id)
            db.session.delete(store)
            db.session.commit()
            return '', 204

    @store_ns.route('/city/<string:city>')
    @store_ns.doc('list_stores_by_city')
    class StoreCity(Resource):
        @store_ns.marshal_list_with(store_model)
        def get(self, city):
            """Fetch stores based on city name"""
            address_url = f"{os.getenv('MM_ADDRESS_URL', 'http://mm-address:5700')}/mm-address/?q={city}"
            address_response = requests.get(address_url)
            if address_response.status_code == 200:
                address_ids = [str(address['id']) for address in address_response.json()]
                stores = Store.query.filter(Store.addressid.in_(address_ids)).all()
                return stores
            return [], 404
