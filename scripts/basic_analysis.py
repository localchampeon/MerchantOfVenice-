def basic_analysis():
    '''
    Merchant Of Venice - Basic Business Metrics
    Quick Exploratory Analysis
    '''
    import pyodbc
    import pandas as pd
    import warnings
    warnings.filterwarnings("ignore", category=UserWarning) #ignore harmless warnings


    #connect to sql server
    conn_str = (
        'DRIVER={SQL Server};'
        'SERVER=DESKTOP-ELTS2E5\SQLEXPRESS;'
        'DATABASE=MerchantOfVenice;'
        'Trusted_connection=yes;'
    )
    conn = pyodbc.connect(conn_str)
    query = '''
    SELECT 
        COUNT(invoice_no) [total_orders],
        COUNT(customer_id) [total_customers],
        SUM(quantity * unit_price) [total_revenue],
        AVG(quantity * unit_price) [avg_transaction_value]
    FROM
        transactions
    '''
    df = pd.read_sql(query, conn)
    print("\n"+"🏛️ OVERALL METRICS:")
    print(df.to_string(index = False))

    #monthly revenue
    query2 = '''
        SELECT 
            YEAR(invoice_date) as year,
            MONTH(invoice_date) as month,
            SUM(quantity * unit_price) as monthly_revenue,
            COUNT(DISTINCT invoice_no) as orders,
            COUNT(DISTINCT customer_id) as active_customers
        FROM 
            transactions
        GROUP BY 
            YEAR(invoice_date), MONTH(invoice_date)
        ORDER BY 
            year, month
    '''
    df2 = pd.read_sql(query2, conn)
    print("\n"+"📈 MONTHLY TRENDS")
    print(df2.to_string(index = False))
    
    query3 = '''
        SELECT TOP 10
        	customer_id,
        	country,
        	total_orders,
        	total_spent
        FROM
        	customers
        ORDER BY
        	total_spent DESC;
    '''
    df3 = pd.read_sql(query3, conn)
    print("\n"+"👑 TOP CUSTOMERS")
    print(df3.to_string(index = False))
    
    query4 = '''
    SELECT TOP 10
    	p.stock_code,
    	MAX(p.description) [description],
    	count(*) total_order,
    	SUM(t.quantity) [total_quantity],
    	SUM(t.quantity * t.unit_price) [total_revenue]
    FROM
    	products as p
    INNER JOIN
    	transactions t
    ON
    	p.stock_code = t.stock_code
    GROUP BY
    	p.stock_code
    ORDER BY
    	SUM(t.quantity * t.unit_price) DESC
    '''
    df4 = pd.read_sql(query4, conn)
    print("\n"+"🛒 TOP PRODUCTS")
    print(df4.to_string(index = False))

    #geographical distribution
    query5 = '''
    SELECT TOP 10
        country,
        COUNT(DISTINCT customer_id) as customers,
        SUM(quantity * unit_price) as revenue
    FROM 
    	transactions
    GROUP BY 
    	country
    ORDER BY 
    	revenue DESC
    '''
    df5 = pd.read_sql(query5, conn)
    print("\n"+"🌍 GEOGRAPHICAL DISTRIBUTION: TOP 10 COUNTRIES")
    print(df5.to_string(index=False))
    return
basic_analysis()
