CREATE DATABASE BIM;
USE BIM;

CREATE TABLE categories (
category_id INT AUTO_INCREMENT PRIMARY KEY, 
name VARCHAR(100) NOT NULL,
description TEXT);

CREATE TABLE suppliers ( 
supplier_id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(150) NOT NULL,
contact_email VARCHAR(100),
phone VARCHAR(20) );

CREATE TABLE inventory (
item_id INT AUTO_INCREMENT PRIMARY KEY,
sku VARCHAR(50) UNIQUE NOT NULL,
name VARCHAR(150) NOT NULL,
category_id INT,
supplier_id INT,
stock_qoh INT NOT NULL DEFAULT 0, 
unit_price DECIMAL(10,2) NOT NULL,
loc VARCHAR(100),
last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
FOREIGN KEY (category_id) REFERENCES categories(category_id),
FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id) );

CREATE TABLE inventory_transactions (
transaction_id INT AUTO_INCREMENT PRIMARY KEY,
item_id INT NOT NULL,
transaction_type ENUM('IN', 'OUT') NOT NULL,
quantity INT NOT NULL,
transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (item_id) REFERENCES inventory(item_id) );



