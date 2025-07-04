from . import db
from datetime import datetime
import json


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.Column(db.Text, nullable=False)  # JSON list
    total = db.Column(db.Float, nullable=False)

    def set_items(self, items_list):
        self.items = json.dumps(items_list)

    def get_items(self):
        return json.loads(self.items)
