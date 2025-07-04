from flask import Blueprint, render_template, request, redirect, url_for
from flask import session
from . import db
from .models import Product, Transaction
from openpyxl import load_workbook

bp = Blueprint('pos', __name__)


def get_cart():
    return session.setdefault('cart', {})


@bp.route('/')
def index():
    products = Product.query.all()
    return render_template('products.html', products=products)


@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            wb = load_workbook(file)
            ws = wb.active
            for row in ws.iter_rows(min_row=2, values_only=True):
                name, price = row[:2]
                if name and price is not None:
                    product = Product(name=str(name), price=float(price))
                    db.session.add(product)
            db.session.commit()
            return redirect(url_for('pos.index'))
    return render_template('upload.html')


@bp.route('/add/<int:product_id>')
def add_to_cart(product_id):
    cart = get_cart()
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session.modified = True
    return redirect(url_for('pos.index'))


@bp.route('/cart')
def view_cart():
    cart = get_cart()
    items = []
    total = 0
    for pid, qty in cart.items():
        product = Product.query.get(int(pid))
        if product:
            subtotal = product.price * qty
            items.append({'product': product, 'qty': qty, 'subtotal': subtotal})
            total += subtotal
    return render_template('cart.html', items=items, total=total)


@bp.route('/checkout', methods=['POST'])
def checkout():
    cart = get_cart()
    items = []
    total = 0
    for pid, qty in cart.items():
        product = Product.query.get(int(pid))
        if product:
            items.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'qty': qty
            })
            total += product.price * qty
    if items:
        tx = Transaction(total=total)
        tx.set_items(items)
        db.session.add(tx)
        db.session.commit()
    session['cart'] = {}
    return redirect(url_for('pos.index'))
