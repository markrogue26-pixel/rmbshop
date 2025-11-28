from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            town TEXT,
            address TEXT,
            name TEXT,
            phone TEXT,
            telegram TEXT,
            product_name TEXT,
            quantity INTEGER
        )
    """)
    conn.commit()
    conn.close()

init_db()

def save_order(town, address, name, phone, telegram, product_name, quantity):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO orders (town, address, name, phone, telegram, product_name, quantity)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (town, address, name, phone, telegram, product_name, quantity))
    conn.commit()
    conn.close()

products = [
    {"category": "Up", "name": "Tshirt 1", "description": "description 1", "image": "images/t-shirts/tshirt1.jpg"},
    {"category": "Up", "name": "Tshirt 2", "description": "description 2", "image": "images/t-shirts/tshirt2.jpg"},
    {"category": "Down", "name": "Jeans 1", "description": "description 3", "image": "images/jeans/jeans1.jpg"},
    {"category": "Down", "name": "Jeans 2", "description": "description 4", "image": "images/jeans/jeans2.jpg"},
    {"category": "Down", "name": "Jeans 3", "description": "description 5", "image": "images/jeans/jeans3.jpg"},
    {"category": "Shoes", "name": "Shoes 3XL", "description": "description 6", "image": "images/shoes/3xl.jpg"},
    {"category": "Shoes", "name": "Track Shoes", "description": "description 7", "image": "images/shoes/track1.jpg"}
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/categories")
def categories():
    return render_template("categories.html", products=products)

@app.route("/buy")
def buy():
    product_name = request.args.get('name')
    product = next((p for p in products if p["name"] == product_name), None)
    if product:
        return render_template("buy.html",
                               product_name=product["name"],
                               product_description=product["description"],
                               product_img=product["image"])
    return "Product not found", 404

@app.route("/order", methods=["POST"])
def order():
    town = request.form["town"]
    address = request.form["address"]
    name = request.form["name"]
    phone = request.form.get("phone", "")
    telegram = request.form.get("telegram", "")
    product_name = request.form["product_name"]
    quantity = int(request.form["quantity"])
    
    save_order(town, address, name, phone, telegram, product_name, quantity)
    return redirect(url_for("categories"))

@app.route("/admin")
def admin():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    data = cursor.fetchall()
    conn.close()
    return render_template("admin.html", orders=data)

if __name__ == "__main__":
    app.run(debug=True)
