import io
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT)

from app import create_app, db
from app.models import Product


def test_upload_and_list(tmp_path):
    db_uri = 'sqlite:///' + str(tmp_path / 'test.db')
    app = create_app({'SQLALCHEMY_DATABASE_URI': db_uri, 'TESTING': True})
    with app.app_context():
        db.create_all()
    client = app.test_client()

    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.append(['name', 'price'])
    ws.append(['Aspirin', 4.5])
    file_stream = io.BytesIO()
    wb.save(file_stream)
    file_stream.seek(0)

    response = client.post(
        '/upload',
        data={'file': (file_stream, 'products.xlsx')},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b'Aspirin' in response.data
    with app.app_context():
        assert Product.query.count() == 1


def test_update_cart(tmp_path):
    db_uri = 'sqlite:///' + str(tmp_path / 'test.db')
    app = create_app({'SQLALCHEMY_DATABASE_URI': db_uri, 'TESTING': True})
    with app.app_context():
        db.create_all()
        prod = Product(name='Ibuprofen', price=2.0)
        db.session.add(prod)
        db.session.commit()
    client = app.test_client()

    client.get('/add/1')
    response = client.post(
        '/update/1',
        data={'qty': '3', 'price': '1.5', 'next': '/cart'},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b'3' in response.data
    assert b'1.50' in response.data

