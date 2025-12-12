def combined_dashboards():
    import pandas as pd
    import plotly.graph_objects as go
    import pyodbc
    from plotly.subplots import make_subplots
    import warnings
    warnings.filterwarnings("ignore", category=UserWarning)

    print("\n"+"This function generates the following charts..")
    print("\n"+"💵 monthly revenue line chart for the year 2011")
    print("\n"+"a pie chart for customer segmentation 📝")
    print("\n"+"a bar chart for TOP performing products 🛒💵")
    print("\n"+"Bar Chart For The Top 10 Countries 🌍 BY Total Revenue and Orders")

    conn_str = (
        'DRIVER={SQL Server};'
        'SERVER=DESKTOP-ELTS2E5\SQLEXPRESS;'
        'DATABASE=MerchantOfVenice;'
        'Trusted_connection=yes;'
    )
    conn = pyodbc.connect(conn_str)

    #query for monthly revenue
    query_revenue_month = """
    SELECT 
        YEAR(t.invoice_date) AS year,
        MONTH(t.invoice_date) AS month,
        MAX(DATENAME(month,t.invoice_date)) [month_name],
        SUM(t.line_total) AS monthly_revenue,
        COUNT(DISTINCT t.invoice_no) AS total_orders,
        COUNT(DISTINCT c.customer_id) AS active_customers
    FROM 
        transactions t
    JOIN
        customers c
    ON
        c.customer_id = t.customer_id
    WHERE Quantity > 0   -- remove returns
    GROUP BY 
        YEAR(t.invoice_date),
        MONTH(t.invoice_date)
    ORDER BY 
        YEAR(t.invoice_date),
        MONTH(t.invoice_date)
    """
    df_revenue_month = pd.read_sql(query_revenue_month, conn)
    df_revenue_month = df_revenue_month[df_revenue_month['year'] == 2011]
    monthly_revenue = go.Scatter(
            x=df_revenue_month['month_name'],          # x-axis: month names
            y=df_revenue_month['monthly_revenue'],     # y-axis: revenue
            text=df_revenue_month['monthly_revenue'],
            name = 'monthly revenue',
            mode = 'lines+markers',# show value on top of bar
            marker_color='royalblue',
            hovertemplate= "Month: %{x}<br>" + "Revenue: %{y:,.2f}<extra></extra>",
            
        )

    #query for customer segments
    query_customer_seg ="""
    SELECT
        segment,
        COUNT(customer_id) customer_count
    FROM
        customer_segments
    GROUP BY 
        segment 
    """
    df_customer_seg = pd.read_sql(query_customer_seg, conn)
    customer_segment = go.Pie(labels = df_customer_seg['segment'], values = df_customer_seg['customer_count'],
                         textinfo= 'percent+label', hole = 0.4)
    #query for top 10 performing products
    query_top_products = """
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
    df_top_products = pd.read_sql(query_top_products, conn)
    df_top_products = df_top_products[::-1]
    top_products = go.Bar(
        y = df_top_products['description'],
        x = df_top_products['revenue'],
        text= df_top_products['description'],
        hovertemplate= "Product: %{y}<br>" + "Revenue: %{x:,.2f}<extra></extra>",
        orientation='h',
        marker=dict(
        color=df_bar["revenue"],
        colorscale="Greens",   # gradient color scale
        showscale=False        # removes color legend
    ))

    #query for top revenue countries
    query_top_countries = """
    SELECT TOP 10
        c.country,
        SUM(t.line_total) total_revenue,
         COUNT(t.invoice_no) [total_orders]
    FROM
        customers c
    JOIN
        transactions t
    ON
        t.customer_id = c.customer_id
    GROUP BY
        c.country
    ORDER BY
        SUM(t.line_total) DESC
    """
    df_top_countries = pd.read_sql(query_top_countries, conn)
    df_top_countries = df_top_countries[::-1]
    top_countries = go.Bar(
        y = df_top_countries['country'],
        x = df_top_countries['total_revenue'],
        text = df_top_countries['total_revenue'],
        orientation = 'h',
        marker=dict(
            color=df_top_countries["total_revenue"],
            colorscale="Blues",   # gradient color scale
            showscale=False      # removes color legend which disrupts the entire fig.
        ),
        customdata=df_top_countries['total_orders'],
        hovertemplate= "<b>%{y}</b><br>" +
            "Revenue: %{x:,.2f}<br>" +
            "Total Orders: %{customdata}<extra></extra>"
    )
    
    query_rfm = """
    SELECT
        customer_id,
        monetary,
        frequency,
        recency_days,
        segment
    FROM 
        customer_segments
    ORDER BY
        monetary DESC
    """
    df_rfm = pd.read_sql(query_rfm, conn)
    segment_cat_color = {
    "Champions": 0,
    "Big Spenders": 1,
    "Loyal": 2,
    "At Risk": 3,
    "Others": 4,
    "Promising":5,
    "Need Attention":6,
    "Lost":7
    }

    df_rfm['segment_color'] = df_rfm['segment'].map(segment_cat_color)
    rfm = go.Scatter(
    x = df_rfm['monetary'],
    y = df_rfm['frequency'],
    mode = 'markers',
    marker=dict(
        size=df_rfm['monetary'] / df_rfm['monetary'].max() * 30, # Normalize bubble sizes    
        # Color by segment instead
        color=df_rfm['segment_color'],
        colorscale='Turbo',
        opacity=0.8,    # Adjust transparency
        line=dict(
            width=1,
            color=df_rfm['segment_color'] # Optional: Add a border to the dots
        )),
    text = df_rfm['customer_id'],
    hovertemplate=
            "<b>Customer:</b> %{text}<br>" +
            "Frequency: %{x}<br>" +
            "Monetary: %{y:,.2f}<br>" +
            "<extra></extra>")

    

    fig = make_subplots(rows=3, cols=2, horizontal_spacing=0.20, subplot_titles=('Monthly Revenue Trend (2011 Only)',
        'Customer Segments', 
        'Top 10 Products',
        'Revenue by Country',
        'RFM Analysis', 'Customer Activity'),
        specs = [[{'type':'scatter'},{'type':'pie'}], #row1
                 [{'type':'bar'},{'type':'bar'}], #row2
                 [{'type':'scatter', "colspan":2},None]] ## Row 3 (spans 2 cols)
                       )
    fig.add_trace(monthly_revenue, row = 1, col =1)
    fig.add_trace(customer_segment, row=1, col=2)
    fig.add_trace(top_products, row = 2, col = 1)
    fig.add_trace(top_countries, row = 2, col = 2)
    fig.add_trace(rfm, row = 3, col = 1)

    fig.update_layout(
        title = {"text":"Merchant Of Venice - E-commerce Analytics Dashboard",
                "x": 0.5, #centralize it
                "xanchor": "center", #sets the horizontal alignment point (anchor) for text, shapes, or annotations relative to their specified x coordinate
                "font":{'size': 24, 'color': '#2c3e50'}},
        height = 1200,
        width = 1200,
        template = "plotly_white",
        showlegend = True
    )

    fig.show()
    fig.write_html("merchant_of_venice_dashboard.html")
    print("Dashboard saved successfully!")
    conn.close()
    return 
combined_dashboards()  
