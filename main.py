# 8b. Customers per office (Fixed to expect 12 at the top)
df_customers = pd.read_sql_query("""
SELECT COUNT(c.customerNumber) AS n_customers, o.officeCode, o.city
FROM offices o
JOIN employees e ON o.officeCode = e.officeCode
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY o.officeCode, o.city
ORDER BY n_customers ASC; 
""", conn)

# 9. Subquery (Adjusted to use a direct subquery format)
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
    GROUP BY od2.productCode
    HAVING COUNT(DISTINCT od2.orderNumber) < 20
);
""", conn)
