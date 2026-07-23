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

        print(user)   # Debug

        if user:

            session["user"] = user[5]
            session["name"] = user[1]

            print(session)

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

        customer = session.get("name")
        print(session)

        # Save Order
        for item in cart:

            cursor.execute(
                """
                INSERT INTO orders
                (customer_name, product_name, quantity, total, payment, address, status)
                VALUES(%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    customer,
                    item["name"],
                    item["qty"],
                    item["price"] * item["qty"],
                    payment,
                    address,
                    "Pending"
                )
            )

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
        cursor.execute("SELECT MAX(order_id) FROM orders")
        order_id = cursor.fetchone()[0]

        print("Order ID =", order_id)




        cursor.execute("SELECT MAX(order_id) FROM orders")
        order_id = cursor.fetchone()[0]

        session["cart"] = []

        return render_template(
            "invoice.html",
            order_id=order_id,
            customer=customer,
            cart=cart,
            total=total,
            payment=payment,
            address=address
        )

    # GET Request
    return render_template(
        "buy.html",
        cart=cart,
        total=total
    )

    


# ===============================
# Run Flask App
# ===============================









    # ===============================
# Profile
# ===============================

@app.route("/profile")
def profile():

    if "user" not in session:
        return redirect("/login")

    cursor.execute(
        "SELECT * FROM customers WHERE username=%s",
        (session["user"],)
    )

    user = cursor.fetchone()

    return render_template("profile.html", user=user)


# ===============================
# Admin Login
# ===============================

@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        cursor.execute(
            "SELECT * FROM admin WHERE username=%s AND password=%s",
            (username, password)
        )

        admin = cursor.fetchone()

        if admin:
            session["admin"] = admin[1]
            return redirect("/dashboard")

        return "Invalid Admin Login"

    return render_template("admin_login.html")

# ===============================
# Dashboard
# ===============================





@app.route("/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect("/admin")

    cursor.execute("SELECT COUNT(*) FROM customers")
    customers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM products")
    products = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders")
    orders = cursor.fetchone()[0]

    # Product List
    cursor.execute("SELECT * FROM products")
    product_list = cursor.fetchall()

    # Order List
    cursor.execute("SELECT * FROM orders")
    order_list = cursor.fetchall()

    print(order_list)   # Debug

    return render_template(
        "admin_dashboard.html",
        customers=customers,
        products=products,
        orders=orders,
        product_list=product_list,
        order_list=order_list
    )
@app.route("/add_product", methods=["GET", "POST"])
def add_product():

    if "admin" not in session:
        return redirect("/admin")

    if request.method == "POST":

        pid = request.form["pid"]
        name = request.form["name"]
        price = request.form["price"]
        stock = request.form["stock"]

        cursor.execute(
            """
            INSERT INTO products(pid, name, price, stock)
            VALUES(%s,%s,%s,%s)
            """,
            (pid, name, price, stock)
        )

        conn.commit()

        return redirect("/dashboard")

    return render_template("add_product.html")

@app.route("/update_status/<int:order_id>", methods=["POST"])
def update_status(order_id):

    if "admin" not in session:
        return redirect("/admin")

    status = request.form["status"]

    print("Order ID:", order_id)
    print("Status:", status)


    cursor.execute(
        "UPDATE orders SET status=%s WHERE order_id=%s",
        (status, order_id)
    )

    conn.commit()

    return redirect("/dashboard")

# ===============================
# Run Flask App
# ===============================

if __name__ == "__main__":
    app.run(debug=True)
