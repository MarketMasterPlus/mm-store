# mm-store/app/schemas.py
from flask_marshmallow import Marshmallow
from .models import Store

ma = Marshmallow()

class StoreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Store
        load_instance = True  # Optional: if true, deserialization will create model instances.

# class StoreSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Store
#         load_instance = True  # Optional: if true, deserialization will create model instances.
