import sqlite3
import pandas as pd

conn = sqlite3.connect('data.sqlite')

# 1. Boston employees (Expects 2 rows, 2 cols: firstName, lastName)
df_boston = pd.read_sql_query("""
SELECT firstName, lastName
FROM employees e
JOIN offices o ON e.officeCode = o.officeCode
WHERE o.city = 'Boston';
""", conn)

# 2. Offices with zero employees (Expects 0 rows)
df_zero_emp = pd.read_sql_query("""
SELECT o.officeCode, o.city
FROM offices o
LEFT JOIN employees e ON o.officeCode = e.officeCode
GROUP BY o.officeCode, o.city
HAVING COUNT(e.employeeNumber) = 0;
""", conn)

# 3. Employees with office city/state (Expects 23 rows, 4 cols)
df_employee = pd.read_sql_query("""
SELECT e.firstName, e.lastName, o.city, o.state
FROM employees e
LEFT JOIN offices o ON e.officeCode = o.officeCode
ORDER BY e.firstName, e.lastName;
""", conn)

# 4. Customers without orders (Expects 24 rows, 4 cols, keeps contactFirstName)
df_contacts = pd.read_sql_query("""
SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
FROM customers c
LEFT JOIN orders o ON c.customerNumber = o.customerNumber
WHERE o.orderNumber IS NULL
ORDER BY c.contactLastName;
""", conn)

# 5. Payments (Expects 273 rows, 4 cols, keeps contactFirstName)
df_payment = pd.read_sql_query("""
SELECT c.contactFirstName, c.contactLastName, p.amount, p.paymentDate
FROM customers c
JOIN payments p ON c.customerNumber = p.customerNumber
ORDER BY CAST(p.amount AS REAL) DESC;
""", conn)

# 6. High credit employees (Expects 4 rows, 4 cols)
df_credit = pd.read_sql_query("""
SELECT e.employeeNumber, e.firstName, e.lastName, COUNT(c.customerNumber) AS num_customers
FROM employees e
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY e.employeeNumber, e.firstName, e.lastName
HAVING AVG(c.creditLimit) > 90000
ORDER BY num_customers DESC;
""", conn)

# 7. Product sold (Expects 109 rows, 3 cols)
df_product_sold = pd.read_sql_query("""
SELECT p.productName, COUNT(DISTINCT o.orderNumber) AS numorders, SUM(od.quantityOrdered) AS totalunits
FROM products p
JOIN orderdetails od ON p.productCode = od.productCode
JOIN orders o ON od.orderNumber = o.orderNumber
GROUP BY p.productName
ORDER BY totalunits DESC;
""", conn)

# 8. Multiple joins - purchasers (Expects 109 rows, 3 cols, expects 'numpurchasers' == 40)
df_total_customers = pd.read_sql_query("""
SELECT p.productName, p.productCode, COUNT(DISTINCT o.customerNumber) AS numpurchasers
FROM products p
JOIN orderdetails od ON p.productCode = od.productCode
JOIN orders o ON od.orderNumber = o.orderNumber
GROUP BY p.productName, p.productCode
ORDER BY numpurchasers DESC;
""", conn)

# 8b. Customers per office (Expects a column named 'n_customers')
df_customers = pd.read_sql_query("""
SELECT COUNT(c.customerNumber) AS n_customers, o.officeCode, o.city
FROM offices o
JOIN employees e ON o.officeCode = e.officeCode
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY o.officeCode, o.city
ORDER BY n_customers DESC;
""", conn)

# 9. Subquery (Expects 15 rows, 5 cols, variable name must be df_under_20)
df_under_20 = pd.read_sql_query("""
SELECT DISTINCT e.employeeNumber, e.firstName, e.lastName, o.city, e.officeCode
FROM employees e
JOIN offices o ON e.officeCode = o.officeCode
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders ord ON c.customerNumber = ord.customerNumber
JOIN orderdetails od ON ord.orderNumber = od.orderNumber
WHERE od.productCode IN (
    SELECT od2.productCode
    FROM orderdetails od2
    JOIN orders o2 ON od2.orderNumber = o2.orderNumber
    GROUP BY od2.productCode
    HAVING COUNT(DISTINCT o2.customerNumber) < 20
);
""", conn)
