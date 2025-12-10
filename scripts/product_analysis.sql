/* PRODUCTS ANALYTICS */
-- 1. Top 10 products by revenue generated (minimum 3 purchase)
SELECT TOP 10
	p.description,
	COUNT(t.invoice_no) [purchase freq],
	SUM(t.line_total) [revenue]
FROM
	products p
JOIN
	transactions t
ON
	p.stock_code = t.stock_code
GROUP BY
	p.description
HAVING
	COUNT(invoice_no) > 3
ORDER BY
	SUM(t.line_total) DESC

-- 2. Top 10 product by quantity sold (minimum 3 purchases)
SELECT TOP 10 
	p.description, 
	SUM(t.quantity) [quantity]
FROM 
	transactions t
JOIN 
	products p
ON 
	p.stock_code = t.stock_code
GROUP BY 
	p.description
HAVING
	COUNT(invoice_no) > 3   use MerchantOfVenice
ORDER BY 
	SUM(t.quantity) DESC

-- 3. Time series for top product (minimum 3 purchases)

SELECT 
	p.stock_code, 
	p.description, 
	CAST(t.invoice_date AS DATE) [date]
FROM 
	transactions t
JOIN 
	products p
ON 
	p.stock_code = t.stock_code
WHERE 
	t.stock_code = (
SELECT TOP 1 stock_code
FROM transactions
GROUP BY stock_code
HAVING COUNT(invoice_no) > 3
ORDER BY SUM(line_total) DESC)
ORDER BY 
	t.invoice_date

--4. Top Products by Consistent Sales Velocity: Monthly Average Quantity Sold
SELECT
    p.description,
    SUM(t.quantity) / COUNT(DISTINCT MONTH(t.invoice_date)) AS avg_monthly_sales
FROM 
	products p
JOIN
	transactions t
ON
	t.stock_code = p.stock_code
GROUP BY 
	p.description
HAVING 
	COUNT(*) >= 3
ORDER BY 
	avg_monthly_sales DESC


-- 5. UNDER PERFORMING PRODUCTS by Low Revenue: Products that generate very little money.
SELECT 
	MAX(p.stock_code) [stock_code],
	p.description,
	SUM(t.line_total) [revenue]
FROM
	products p
JOIN
	transactions t
ON
	p.stock_code = t.stock_code
GROUP BY
	p.description
HAVING 
	SUM(t.line_total) < (SELECT AVG(line_total) FROM transactions)
ORDER BY
	SUM(t.line_total) ASC

-- 6. Underperforming by Low Sales Volume: Products customers rarely buy — low total quantity.
SELECT 
	MAX(p.stock_code) [stock_code],
	p.description,
	SUM(t.quantity) [quantity]
FROM
	products p
JOIN
	transactions t
ON
	p.stock_code = t.stock_code
GROUP BY
	p.description
HAVING 
	SUM(t.quantity) < (SELECT AVG(quantity) FROM transactions)
ORDER BY
	SUM(t.quantity) ASC

-- 7. Underperforming by Low Purchase Frequency: Products that appear in very few orders.
SELECT 
	MAX(p.stock_code) [stock_code],
	p.description,
	COUNT(t.invoice_no) [frequency] 
FROM
	products p
JOIN
	transactions t
ON
	p.stock_code = t.stock_code
GROUP BY
	p.description
HAVING 
	COUNT(t.invoice_no) < (SELECT AVG(counts) FROM (SELECT COUNT(invoice_no) counts FROM transactions GROUP BY stock_code )t)
ORDER BY
	COUNT(t.invoice_no) ASC

-- 8. Underperforming by Slow Sales Velocity: Products that sell slowly over time (useful for time-series analysis).
SELECT TOP 10
    p.description,
    SUM(t.quantity) / COUNT(DISTINCT MONTH(t.invoice_date)) AS avg_monthly_sales
FROM 
	products p
JOIN
	transactions t
ON
	t.stock_code = p.stock_code
GROUP BY p.description
ORDER BY avg_monthly_sales ASC;
