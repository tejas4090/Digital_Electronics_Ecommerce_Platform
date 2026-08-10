# 🛒 Digital Electronics E-Commerce Platform

## 📌 Project Overview

The **Digital Electronics E-Commerce Platform** is a web-based online shopping application developed using **Python Flask, MySQL, HTML5, CSS3, and JavaScript**.

The system is designed to provide a simple and user-friendly platform for purchasing digital and electronic products online.

Customers can create an account, verify their email using **OTP verification**, log in securely, browse and search products, view product details, add products to the shopping cart, place orders, generate invoices, track orders, and submit product reviews.

The application also provides an **Admin Panel** through which administrators can manage products, customers, and orders.

-------------------------------------------------------------------------------------------------------------------------------------

## 🚀 Features

### 👤 Customer Module

* User Registration
* Email OTP Verification
* Secure Login
* Forgot Password using OTP
* Password Reset
* Product Search
* Product Listing
* Product Details
* Add Products to Cart
* Remove Products from Cart
* Buy Products
* Order Placement
* Order Invoice
* Order Tracking
* Product Reviews and Ratings
* User Profile
* Logout
* Order Confirmation Email

-------------------------------------------------------------------------------------------------------------------------------------

### 🔐 Admin Module

* Admin Login
* Admin Dashboard
* View Customers
* View Customer Details
* Manage Products
* Add Products
* Update Products
* Delete Products
* View Orders
* Update Order Status
* Monitor Product Stock

-------------------------------------------------------------------------------------------------------------------------------------

## 📧 Email & OTP Features

The application uses **Gmail SMTP** for email communication.

### Registration

1. Customer enters registration details.
2. System generates a six-digit OTP.
3. OTP is sent to the customer's registered email.
4. Customer enters the OTP.
5. After successful verification, the account is created.

### Forgot Password

1. Customer enters the registered email.
2. System generates an OTP.
3. OTP is sent through email.
4. Customer verifies the OTP.
5. Customer creates a new password.

### Order Confirmation

After successfully placing an order, the system sends an order confirmation email containing:

* Customer Name
* Total Amount
* Payment Method
* Delivery Address
* Order Status

-------------------------------------------------------------------------------------------------------------------------------------

## 🛠 Technologies Used

| Technology     | Purpose                     |
| -------------- | --------------------------- |
| **Python**     | Backend programming         |
| **Flask**      | Web application framework   |
| **HTML5**      | Web page structure          |
| **CSS3**       | Website styling             |
| **JavaScript** | Client-side functionality   |
| **MySQL**      | Database management         |
| **Gmail SMTP** | OTP and email notifications |

-------------------------------------------------------------------------------------------------------------------------------------

## 📂 Project Structure

```text
Digital_Electronics_Ecommerce_Platform/
│
├── app.py
├── database.sql
├── requirements.txt
├── README.md
│
├── static/
│   ├── style.css
│   └── images/
└── templates/
    ├── index.html
    ├── register.html
    ├── login.html
    ├── otp.html
    ├── otp_success.html
    ├── forgot_password.html
    ├── forgot_verify_otp.html
    ├── reset_password.html
    ├── password_success.html
    ├── products.html
    ├── product_details.html
    ├── cart.html
    ├── buy.html
    ├── invoice.html
    ├── orders.html
    ├── track_order.html
    ├── profile.html
    ├── success.html
    │
    ├── admin_login.html
    ├── admin_dashboard.html
    ├── admin_customers.html
    ├── add_product.html
    ├── update_product.html
    └── delete_product.html
```

-------------------------------------------------------------------------------------------------------------------------------------

## 🗄️ Database

The project uses **MySQL** as the database management system.

### Database Name

```text
online_shopping
```

### Main Tables

#### 👤 Customers

Stores customer registration and account information.

```text
customers
```

#### 📦 Products

Stores electronic product information such as:

* Product ID
* Product Name
* Price
* Stock

```text
products
```

#### 🛍️ Orders

Stores customer order information such as:

* Order ID
* Customer Name
* Product Name
* Quantity
* Total Amount
* Payment Method
* Address
* Order Date

```text
orders
```

#### ⭐ Reviews

Stores customer product reviews and ratings.

```text
reviews
```

-------------------------------------------------------------------------------------------------------------------------------------

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/tejas4090/Digital_Electronics_Ecommerce_Platform.git
```

### 2. Open the Project Folder

```bash
cd Digital_Electronics_Ecommerce_Platform
```

### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

  The main dependencies are:

  ```text
  Flask
  gunicorn
  mysql-connector-python
  ```

> 
### 4. Run the Application

```bash
python app.py
```

### 5. Open in Browser

```text
http://127.0.0.1:5000/
```

---

## 🔄 Application Workflow

### Customer Workflow

```text
Home Page
    ↓
Register
    ↓
Email OTP Verification
    ↓
Registration Successful
    ↓
Login
    ↓
Products
    ↓
Search / View Product
    ↓
Product Details
    ↓
Add to Cart
    ↓
Cart
    ↓
Buy / Checkout
    ↓
Place Order
    ↓
Invoice
    ↓
Order Tracking
```

-------------------------------------------------------------------------------------------------------------------------------------

### Forgot Password Workflow

```text
Login
   ↓
Forgot Password
   ↓
Enter Registered Email
   ↓
OTP Sent to Email
   ↓
Verify OTP
   ↓
Reset Password
   ↓
Password Updated
   ↓
Login
```

-------------------------------------------------------------------------------------------------------------------------------------

### Admin Workflow

```text
Admin Login
     ↓
Admin Dashboard
     ↓
 ┌───────────────┬───────────────┬───────────────┐
 ↓               ↓               ↓
Customers      Products        Orders
 ↓               ↓               ↓
View          Add / Update     View Orders
Customers       / Delete          ↓
                                Update
                              Order Status
```

-------------------------------------------------------------------------------------------------------------------------------------

## 🛍️ Product Management

The admin can manage electronic products from the Admin Panel.

### Admin can:

* Add new products
* Update existing products
* Delete products
* View product information
* Manage available stock

Customers can then view the products from the product section.

-------------------------------------------------------------------------------------------------------------------------------------

## 📦 Order Management

Customers can:

* Add products to cart
* Select quantity
* Place orders
* View order details
* Generate invoice
* Track order status

The admin can view customer orders and update their order status.

-------------------------------------------------------------------------------------------------------------------------------------

## 🔐 Authentication

The application provides authentication features including:

* Customer Registration
* Email OTP Verification
* Login
* Forgot Password
* OTP Verification
* Password Reset
* Session Management
* Logout

-------------------------------------------------------------------------------------------------------------------------------------

## 🎯 Project Objectives

The main objectives of this project are:

1. To develop a simple online shopping platform for digital electronics.
2. To provide secure customer registration and login.
3. To implement email-based OTP verification.
4. To provide product searching and browsing functionality.
5. To implement shopping cart and order management.
6. To generate customer invoices.
7. To provide order tracking functionality.
8. To allow customers to submit reviews and ratings.
9. To provide an admin panel for managing the e-commerce system.
10. To demonstrate the practical implementation of Flask and MySQL.

-------------------------------------------------------------------------------------------------------------------------------------

## 🔮 Future Scope

The project can be further improved by adding:

* Online Payment Gateway
* Product Categories
* Wishlist
* Product Filtering and Sorting
* Advanced Admin Dashboard
* Sales Reports and Analytics
* Stock Alerts
* Multiple Product Images
* Secure Password Hashing
* Environment Variable Configuration
* REST API Integration
* Deployment on a Cloud Platform

-------------------------------------------------------------------------------------------------------------------------------------

## 📚 Learning Outcomes

Through this project, we learned:

* Python Flask Web Development
* MySQL Database Connectivity
* HTML and CSS Web Design
* JavaScript Integration
* CRUD Operations
* Session Management
* Email SMTP Integration
* OTP Authentication
* E-Commerce Workflow
* Git and GitHub
* Frontend and Backend Integration

-------------------------------------------------------------------------------------------------------------------------------------

## 👨‍💻 Developed By

- **Tejas Shinde**
- **Anish Shelar**
- **Avishkar Shendage**
- **Samarth Mitkari**
- **Shivraj Sable**
- **Aadity Gawali**

**Diploma in Computer Technology**  
**Government Polytechnic Pen**

-------------------------------------------------------------------------------------------------------------------------------------

## 📄 License

This project is developed for **educational purposes** as part of the Diploma in Computer Technology program.

-------------------------------------------------------------------------------------------------------------------------------------



