# POSf

A minimal point-of-sale web application for a pharmacy built with Flask. It can load products from an Excel sheet, create a shopping cart and store transactions.

## Setup

Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the application:

```bash
python run.py
```

Open `http://localhost:5000` in your browser.

## Loading products

Use the **Upload** page to load an Excel file. The file should contain two columns: `name` and `price`. The first row is treated as the header.

You can also pre-populate the database by providing the path to an Excel
workbook using the `LOAD_PRODUCTS_FILE` configuration option. For example, to
load a sheet called *Listado de Precios.xlsx* at start up, run:

```bash
export LOAD_PRODUCTS_FILE="/path/to/Listado de Precios.xlsx"
python run.py
```

## Running tests

```
pytest
```
