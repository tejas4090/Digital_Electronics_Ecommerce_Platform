# 🛒 Digital Electronics E-Commerce Platform

## 📌 Project Overview

The Digital Electronics E-Commerce Platform is a web-based application developed using Python Flask and MySQL. It allows customers to register, verify their account using Email OTP, browse electronic products, add items to the cart, place orders, and receive order confirmation emails. The platform also provides an admin panel for managing products, customers, and orders.

---

## 🚀 Features

### Customer
- User Registration with Email OTP Verification
- Secure Login
- Forgot Password via OTP
- Product Search
- Product Details
- Add to Cart
- Buy Products
- Order Invoice
- Order Tracking
- Product Reviews
- User Profile
- Order Confirmation Email

### Admin
- Admin Login
- Dashboard
- Manage Products
- View Customers
- View Orders
- Update Order Status
- Add Products 

---

## 🛠 Technologies Used

- Python
- Flask
- HTML5
- CSS3
- JavaScript
- MySQL
- Gmail SMTP

---

## 📂 Project Structure

```
Digital_Electronics_Ecommerce_Platform/
│
├── app.py
├── requirements.txt
├── database.sql
├── static/
│   ├── style.css
│   ├── images/
│   
│
├── templates/
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── products.html
│   ├── product_details.html
│   ├── cart.html
│   ├── buy.html
│   ├── invoice.html
│   ├── profile.html
│   ├── otp.html
│   ├── otp_success.html
│   ├── forgot_password.html
│   ├── forgot_verify_otp.html
│   ├── reset_password.html
│   ├── password_success.html
│   ├── admin_login.html
│   ├── admin_dashboard.html
│   ├── admin_customers.html
│   └── add_product.html
```

---

## ⚙ Installation

1. Clone the repository

```bash
git clone https://github.com/tejas4090/Digital_Electronics_Ecommerce_Platform.git
```

2. Open the project folder

```bash
cd Digital_Electronics_Ecommerce_Platform
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Import the MySQL database.

5. Update database credentials in `app.py`.

6. Run the application

```bash
python app.py
```

7. Open in browser

```
http://127.0.0.1:5000/
```

---

## 📧 Email Features

- Registration OTP Verification
- Forgot Password OTP
- Order Confirmation Email

---

## 👨‍💻 Developed By

**Tejas Shinde**

Diploma in Computer Technology

Government Polytechnic Pen 

---

## 📄 License

This project is developed for educational purposes.