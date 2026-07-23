from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "shopping123"

# ===============================
# MySQL Connection
# ===============================

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="****",
    password="*****",
    database="online_shopping"
)

cursor = conn.cursor()

# ===============================
# Home Page
# ===============================

@app.route("/")
def home():
   return render_template("index.html")

# ===============================
# Register
# ===============================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        mobile = request.form["mobile"]
        address = request.form["address"]
        pincode = request.form["pincode"]
        username = request.form["username"]
        password = request.form["password"]

        sql = """
        INSERT INTO customers
        (name,mobile,address,pincode,username,password)
        VALUES(%s,%s,%s,%s,%s,%s)
        """

        values = (
            name,
            mobile,
            address,
            pincode,
            username,
            password
        )

        try:

            cursor.execute(sql, values)
            conn.commit()

            return redirect("/login")

        except mysql.connector.Error:
            return "Username already exists!"

    return render_template("register.html")

# ===============================
# Login
# ===============================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        cursor.execute(
            """
            SELECT * FROM customers
            WHERE username=%s
            AND password=%s
            """,
            (username, password)
        )

        user = cursor.fetchone()

        if user:

            session["user"] = user[1]

            return redirect("/products")

        else:

            return "Invalid Username or Password"

    return render_template("login.html")

# ===============================
# Products Page
# ===============================

@app.route("/products")
def products():

    cursor.execute("SELECT * FROM products")

    products = cursor.fetchall()

    return render_template(
        "products.html",
        products=products
    )


# ===============================
# Add To Cart
# ===============================

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():

    pid = request.form["pid"]
    qty = int(request.form["qty"])

    cursor.execute(
        "SELECT * FROM products WHERE pid=%s",
        (pid,)
    )

    product = cursor.fetchone()

    if product is None:
        return "Product Not Found"

    if qty > product[3]:
        return "Stock Not Available"

    if "cart" not in session:
        session["cart"] = []

    cart = session["cart"]

    cart.append({
        "pid": product[0],
        "name": product[1],
        "price": float(product[2]),
        "qty": qty
    })

    session["cart"] = cart

    return redirect("/cart")


# ===============================
# View Cart
# ===============================

@app.route("/cart")
def cart():

    cart_items = session.get("cart", [])

    total = 0

    for item in cart_items:
        total += item["price"] * item["qty"]

    return render_template(
        "cart.html",
        cart=cart_items,
        total=total
    )


# ===============================
# Remove From Cart
# ===============================

@app.route("/remove/<int:pid>")
def remove(pid):

    cart = session.get("cart", [])

    new_cart = []

    for item in cart:

        if item["pid"] != pid:
            new_cart.append(item)

    session["cart"] = new_cart

    return redirect("/cart")


# ===============================
# Logout
# ===============================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")
# ===============================
# Buy Now / Checkout
# ===============================

@app.route("/buy", methods=["GET", "POST"])
def buy():

    cart = session.get("cart", [])

    if len(cart) == 0:
        return "Your Cart is Empty!"

    total = 0

    for item in cart:
        total += item["price"] * item["qty"]

    if request.method == "POST":

        payment = request.form["payment"]
        address = request.form["address"]

        customer = session.get("user")

        # Save Order
        for item in cart:

            cursor.execute(
                """
                INSERT INTO orders
                (customer_name, product_name, quantity, total, payment, address)
                VALUES(%s,%s,%s,%s,%s,%s)
                """,
                (
                    customer,
                    item["name"],
                    item["qty"],
                    item["price"] * item["qty"],
                    payment,
                    address
                )
            )

            # Update Stock
            cursor.execute(
                """
                UPDATE products
                SET stock = stock - %s
                WHERE pid = %s
                """,
                (
                    item["qty"],
                    item["pid"]
                )
            )

        conn.commit()

        session["cart"] = []

        return render_template(
            "orders.html",
            total=total,
            payment=payment
        )

    return render_template(
        "buy.html",
        cart=cart,
        total=total
    )


# ===============================
# Run Flask App
# ===============================

if __name__ == "__main__":
    app.run(debug=True)






    