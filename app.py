import smtplib
import random
from email.mime.text import MIMEText

#===============================

from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "shopping123"

#===============================

def send_otp(receiver_email, otp, purpose="registration"):

    sender_email = "demo234409@gmail.com"
    app_password = "******"

    if purpose == "forgot":
        subject = "Forgot your Digital Electronics Password By OTP"
        body = f"Your OTP to reset your password is: {otp}"
    else:
        subject = "Digital Electronics OTP Verification"
        body = f"Your OTP for registration is: {otp}"

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, app_password)

    server.send_message(msg)

    server.quit()
    print("OTP Sent To Mail Successfully")


#===============================

def send_order_email(receiver_email, customer_name, total, payment, address):

    sender_email = "demo234409@gmail.com"
    app_password = "*******"

    body = f"""
Hello {customer_name},

🎉 Thank you for shopping with Digital Electronics E-Commerce Platform.

Your order has been placed successfully.

==============================
Order Details
==============================

Customer Name : {customer_name}

Total Amount : ₹{total}

Payment Method : {payment}

Delivery Address :
{address}

Order Status : Pending

Thank you for shopping with us.

Digital Electronics E-Commerce Platform
"""

    msg = MIMEText(body)

    msg["Subject"] = "Order Confirmation"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, app_password)
    
    

    server.sendmail(
        sender_email,
        receiver_email,
        msg.as_string()
    )

    server.quit()

    

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
        email = request.form["email"]
        address = request.form["address"]
        pincode = request.form["pincode"]
        username = request.form["username"]
        password = request.form["password"]

        otp = random.randint(100000, 999999)

        session["otp"] = str(otp)

        session["register_data"] = {
            "name": name,
            "mobile": mobile,
            "email": email,
            "address": address,
            "pincode": pincode,
            "username": username,
            "password": password
        }

        print("Email from form:", email)

        send_otp(email, otp)

        return redirect("/verify_otp")

    return render_template("register.html")

#--------------------------------


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        cursor.execute(
            """
            SELECT * FROM customers
            WHERE username=%s AND password=%s
            """,
            (username, password)
        )

        user = cursor.fetchone()

        if user:

            session["user"] = user[6]   # username
            session["name"] = user[1]   # name

            return redirect("/products")

        return render_template(
    "login.html",
    error="Invalid Username or Password!"
)

    return render_template("login.html")

#=============================

@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":

        email = request.form["email"].strip()

        cursor.execute("SELECT * FROM customers")
        users = cursor.fetchall()

        print(users)

        # Email Check
        found = False

        for user in users:
            if user[3].strip().lower() == email.lower():
                found = True
                break

        if found:

            otp = random.randint(100000, 999999)

            session["forgot_otp"] = str(otp)
            session["forgot_email"] = email

            send_otp(email, otp, "forgot")

            return redirect("/forgot_verify_otp")

        else:

            return "Email Not Registered!"

    return render_template("forgot_password.html")

    #=============================

@app.route("/forgot_verify_otp", methods=["GET", "POST"])
def forgot_verify_otp():

    if request.method == "POST":

        user_otp = request.form["otp"]

        if user_otp == session.get("forgot_otp"):

            return redirect("/reset_password")

        else:

            return "Invalid OTP!"

    return render_template("forgot_verify_otp.html")

    #=============================

@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():

    if request.method == "POST":

        new_password = request.form["password"]

        email = session.get("forgot_email")

        cursor.execute(
            """
            UPDATE customers
            SET password=%s
            WHERE email=%s
            """,
            (new_password, email)
        )

        conn.commit()

        session.pop("forgot_otp", None)
        session.pop("forgot_email", None)

        return render_template("password_success.html")

    return render_template("reset_password.html")

#--------------------------------

@app.route("/verify_otp", methods=["GET", "POST"])
def verify_otp():

    if request.method == "POST":

        user_otp = request.form["otp"]
        saved_otp = session.get("otp")

        if saved_otp is None:
            return "OTP Session Expired. Please Register Again."

        if user_otp != saved_otp:
            return "Invalid OTP!"

        data = session.get("register_data")

        if data is None:
            return "Registration Data Not Found."

        sql = """
        INSERT INTO customers
        (name, mobile, email, address, pincode, username, password)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            data["name"],
            data["mobile"],
            data["email"],
            data["address"],
            data["pincode"],
            data["username"],
            data["password"]
        )

        try:

            cursor.execute(sql, values)
            conn.commit()
            print("Customer Saved Successfully")


            session.pop("otp", None)
            session.pop("register_data", None)

            print("Redirecting to Login...")    

            return render_template("otp_success.html")

        except mysql.connector.Error as e:
            print("MYSQL ERROR:", e)
            return f"MySQL Error: {e}"

    return render_template("otp.html")  
# ===============================
# Products Page
# ===============================

@app.route("/products")
def products():

    if "user" not in session:
        return redirect("/login")

    search = request.args.get("search", "")

    if search:

        cursor.execute("""
             SELECT * FROM products
            WHERE name LIKE %s
            """, ("%" + search + "%",))

    else:

        cursor.execute("SELECT * FROM products")

    products = cursor.fetchall()

    return render_template(
        "products.html",
        products=products,
        search=search
    )

@app.route("/product/<int:pid>")
def product_details(pid):

    cursor.execute(
        "SELECT * FROM products WHERE pid=%s",
        (pid,)
    )

    product = cursor.fetchone()

    cursor.execute(
        "SELECT * FROM reviews WHERE product_id=%s",
        (pid,)
    )
    reviews = cursor.fetchall()

    return render_template(
    "product_details.html",
    product=product,
    reviews=reviews
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

@app.route("/add_review", methods=["POST"])
def add_review():

    if "user" not in session:
        return redirect("/login")

    product_id = request.form["product_id"]
    rating = request.form["rating"]
    review = request.form["review"]
    username = session["user"]

    cursor.execute("""
        INSERT INTO reviews
        (product_id, username, rating, review)
        VALUES (%s,%s,%s,%s)
    """, (product_id, username, rating, review))

    conn.commit()

    return redirect("/product/" + product_id)
    


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

@app.route("/track_order")
def track_order():

    if "user" not in session:
        return redirect("/login")

    cursor.execute(
        """
        SELECT order_id,
               product_name,
               quantity,
               total,
               payment,
               status
        FROM orders
        WHERE customer_name=%s
        ORDER BY order_id DESC
        """,
        (session["name"],)
    )

    orders = cursor.fetchall()

    return render_template(
        "track_order.html",
        orders=orders
    )
# ===============================
# Buy Now / Checkout
# ===============================

@app.route("/buy", methods=["GET", "POST"])
def buy():

    if "user" not in session:
        return redirect("/login")

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

        # Customer Email Get
        cursor.execute(
            "SELECT email FROM customers WHERE username=%s",
            (session["user"],)
        )

        result = cursor.fetchone()

        if result:
            customer_email = result[0]
        else:
            customer_email = ""

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

        # ===============================
        # Send Order Confirmation Email
        # ===============================

        if customer_email != "":

            send_order_email(
                customer_email,
                customer,
                total,
                payment,
                address
            )

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

        return render_template(
    "admin_login.html",
    error="Invalid Admin Username or Password!"
)

    return render_template("admin_login.html")



@app.route("/admin/customers")
def admin_customers():

    if "admin" not in session:
        return redirect("/admin")

    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()

    return render_template(
        "admin_customers.html",
        customers=customers
    )

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
        image = request.form["image"]

        cursor.execute(
            """
            INSERT INTO products(pid, name, price, stock, image)
            VALUES(%s,%s,%s,%s,%s)
            """,
            (pid, name, price, stock, image)
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
