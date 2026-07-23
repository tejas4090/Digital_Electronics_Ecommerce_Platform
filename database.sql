CREATE DATABASE IF NOT EXISTS online_shopping;

USE online_shopping;

-- Customers Table
CREATE TABLE customers (
    cid INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    mobile VARCHAR(15) NOT NULL,
    address VARCHAR(255) NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);

-- Products Table
CREATE TABLE products (
    pid INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL
);

-- Orders Table
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100),
    product_name VARCHAR(100),
    quantity INT,
    total DECIMAL(10,2),
    payment VARCHAR(30),
    address VARCHAR(255),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert Products
INSERT INTO products (pid, name, price, stock) VALUES
(1, 'Laptop', 50000, 10),
(2, 'Mobile', 20000, 15),
(3, 'Headphones', 1500, 20),
(4, 'Keyboard', 1200, 25),
(5, 'Mouse', 800, 30),
(6, 'Monitor', 15000, 8);