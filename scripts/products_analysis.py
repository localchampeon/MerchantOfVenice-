import pandas as pd
import pyodbc
def products_analytics():
    '''
    this function connects to the local database to run some sql script.
    it prints a basic analytics report onproducts performance.
    '''
    conn_str = (
        'DRIVER={SQL Server};'
        'SERVER=DESKTOP-ELTS2E5\SQLEXPRESS;'
        'DATABASE=MerchantOfVenice;'
        'Trusted_connection=yes;'
    )
    conn = pyodbc.connect(conn_str)

    print("\n"+"🛒Products Analytics📊")
    print("\n"+"-- Top 10 products 🛒 by revenue generated 💵 (minimum 3 purchase)")
    query0 = """
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
    """
    df0 = pd.read_sql(query0, conn)
    print(df0.to_string(index=False))

    print("\n"+"Top 10 product🛒 by quantity sold📈💰📊 (minimum 3 purchases)")
    query1 = """
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
    	COUNT(invoice_no) > 3
    ORDER BY 
    	SUM(t.quantity) DESC
    """
    df1 = pd.read_sql(query1, conn)
    print(df1.to_string(index = False))

    print("\n"+"--Time series 🕒📊 for top product🏆 by revenue 💵 (minimum 3 purchases). First 20 buys")
    query2 = """
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
    """
    df2 = pd.read_sql(query2, conn)
    print(df2.head(20).to_string(index=False))

    print("\n"+"Top 10 Products 🛒 by Consistent Sales Velocity 🚀: Monthly Average Quantity Sold")
    query3 = """
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
    """
    df3 = pd.read_sql(query3, conn)
    print(df3.head(10).to_string(index=False))

    print("\n"+"📉💵 TOP 10 UNDER PERFORMING PRODUCTS by Low Revenue: Products that generate very little money.")
    query4 = """
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
    """
    df4 = pd.read_sql(query4, conn)
    print(df4.head(10).to_string(index = False))

    print("\n"+"🛒📉 Underperforming by Low Sales Volume: Products customers rarely buy — low total quantity.")
    query5 = """
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
    """
    df5 = pd.read_sql(query5, conn)
    print(df5.head(10).to_string(index=False))

    print("\n"+"📉🛒 TOP 10 Underperforming by Low Purchase Frequency: Products that appear in very few orders.")
    query5 = """
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
    """
    df5 = pd.read_sql(query5, conn)
    print(df5.head(10).to_string(index=False))

    print("\n"+"🕒📉 TOP 10 Underperforming by Slow Sales Velocity: Products that sell slowly over time (useful for time-series analysis).")
    query6 = """
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
        """
    df6 = pd.read_sql(query6, conn)
    print(df6.head(10).to_string(index=False))
products_analytics()
