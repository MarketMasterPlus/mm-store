# mm-store/app/api/routes.py
from flask import request
from flask_restx import Resource, fields, Namespace
from ..models import db, Store
from ..schemas import StoreSchema
import requests
import os

def init_routes(api):
    store_ns = Namespace('stores', description='Store operations')
    api.add_namespace(store_ns, path='/mm-store')

    store_model = api.model('Store', {
        'id': fields.Integer(readOnly=True, description='The unique identifier of a store'),
        'ownerid': fields.String(required=True, description='The CPF identifier of the store owner'),
        'cnpj': fields.String(required=True, description='CNPJ of the store'),
        'name': fields.String(required=True, description='Store commercial name'),
        'imageurl': fields.String(required=False, description='URL of the store image'),
        'addressid': fields.String(readOnly=True, description='The unique identifier of the store address'),
        # Add address fields
        'cep': fields.String(required=True, description='Postal code'),
        'street': fields.String(required=True, description='Street name'),
        'number': fields.String(required=False, description='House number'),
        'neighborhood': fields.String(required=True, description='Neighborhood'),
        'state': fields.String(required=True, description='State name'),
        'city': fields.String(required=True, description='City name'),
        'complement': fields.String(description='Complement information')
    })

    @store_ns.route('/')
    class StoreList(Resource):
        @store_ns.doc('list_stores')
        @store_ns.marshal_list_with(store_model)
        def get(self):
            query = request.args.get('q')
            if query:
                search_filter = f"%{query.lower()}%"
                stores = Store.query.filter(
                    db.or_(
                        db.func.lower(Store.name).ilike(search_filter),
                        db.func.lower(Store.cnpj).ilike(search_filter)
                    )
                ).all()
            else:
                stores = Store.query.all()
            return stores

        @store_ns.doc('create_store')
        @store_ns.expect(store_model)
        @store_ns.marshal_with(store_model, code=201)
        def post(self):
            data = request.json
            address_data = {
                'cep': data['cep'],
                'street': data['street'],
                'number': data['number'],
                'neighborhood': data['neighborhood'],
                'state': data['state'],
                'city': data['city'],
                'complement': data.get('complement', '')
            }
            address_url = f"{os.getenv('MM_ADDRESS_URL', 'http://mm-address:5700')}/mm-address"
            response = requests.post(address_url, json=address_data)
            if response.status_code == 201:
                address_id = response.json()['id']
                store = Store(
                    ownerid=data['ownerid'],
                    addressid=address_id,
                    cnpj=data['cnpj'],
                    name=data['name'],
                    imageurl=data.get('imageurl')
                )
                db.session.add(store)
                db.session.commit()
                return store, 201
            else:
                return {'message': 'Failed to create address', 'details': response.json()}, response.status_code

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
            """Update a store and its address"""
            store = Store.query.get_or_404(id)
            data = request.json

            # Update store information
            for key in ['ownerid', 'cnpj', 'name', 'imageurl']:
                if key in data:
                    setattr(store, key, data[key])

            # Check if address data is provided and if changes are made, update the address
            address_fields = ['cep', 'street', 'number', 'neighborhood', 'state', 'city', 'complement']
            address_data = {field: data[field] for field in address_fields if field in data}
            if address_data:
                address_url = os.getenv('MM_ADDRESS_URL', 'http://mm-address:5700') + f'/mm-address/{store.addressid}'
                address_response = requests.put(address_url, json=address_data)
                if address_response.status_code != 200:
                    return {'message': 'Failed to update address'}, address_response.status_code

            # Commit changes to the database
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
                # Ensure address IDs are integers
                address_ids = [str(address['id']) for address in address_response.json()]
                stores = Store.query.filter(Store.addressid.in_(address_ids)).all()
                return stores
            return [], 404
