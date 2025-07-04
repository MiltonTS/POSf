import os
from app import create_app

config = {}
if os.environ.get('LOAD_PRODUCTS_FILE'):
    config['LOAD_PRODUCTS_FILE'] = os.environ['LOAD_PRODUCTS_FILE']

app = create_app(config)

if __name__ == '__main__':
    app.run(debug=True)
