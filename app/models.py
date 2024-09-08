# mm-store/app/models.py

from . import db  # Import the db instance from __init__.py

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ownerid = db.Column(db.String(255), nullable=False)
    addressid = db.Column(db.Integer, nullable=False)
    cnpj = db.Column(db.String(14), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    imageurl = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Store {self.name}, {self.cnpj}>"
