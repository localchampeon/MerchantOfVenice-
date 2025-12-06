import pandas as pd
import pyodbc

#conncet to local sql server
def load_transcations(data):
    conn_str = (
        'DRIVER={SQL Server};'
        'SERVER=DESKTOP-ELTS2E5\SQLEXPRESS;'  # CHANGE THIS!
        'DATABASE=MerchantOfVenice;'
        'Trusted_Connection=yes;'
    )
    
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    #INSERT TRANSACTIONS
    try:
        print("Inserting transactions...")
        
        for index, row in data.iterrows():
            cursor.execute("""
                INSERT INTO transactions 
                (invoice_no, stock_code, description, quantity, invoice_date, 
                 unit_price, customer_id, country)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, 
            row['InvoiceNo'], 
            row['StockCode'], 
            row['Description'], 
            int(row['Quantity']), 
            row['InvoiceDate'], 
            float(row['UnitPrice']), 
            row['CustomerID'], 
            row['Country']
            )
            if index % 100000 == 0:
                print(f"Processed {index} rows...")
                conn.commit()
    
        conn.commit()
        conn.close
        print("✅ Data loaded!")
        return
        
    except Exception as e:
        print("An error occured !!!"+ "\n" f"{e}")
        print("\n"+ f"exception type {type(e)}")
        conn.close()
        return

#load customer table
def load_customers():
    #connect to sql server
    conn_str = (
        'DRIVER={SQL Server};'
        'SERVER=DESKTOP-ELTS2E5\SQLEXPRESS;'
        'DATABASE=MerchantOfVenice;'
        'Trust_connection=yes;'
    ) #note the absence of white spaces
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    #insert transactions
    try:
        print('Inserting transaction...')
        cursor.execute(
            '''
            INSERT INTO customers
            (customer_id,country,first_purchase_date,last_purchase_date,total_orders, total_spent)
            SELECT
                customer_id,
                MAX(country),
                MIN(invoice_date),
                MAX(invoice_date),
                SUM(quantity),
                SUM(unit_price)
            FROM
                transactions
            GROUP BY customer_id        
                ''')
        conn.commit()
        conn.close()
        print('cutomers table successfully loaded✅')
        return
    except Exception as e:
        print("An error occured !!!"+ "\n" f"{e}")
        print("\n"+ f"exception type {type(e)}")
        conn.close()
        return

#load data into products
def load_products():
    conn_str = (
        'DRIVER={SQL Server};'
        'SERVER=DESKTOP-ELTS2E5\SQLEXPRESS;'
        'DATABASE=MerchantOfVenice;'
        'Trust_connection=yes;'
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    try:
        cursor.execute(
            '''
            INSERT INTO products
            (stock_code,description,unit_price)
            SELECT
            	stock_code,
            	MAX(description),
            	SUM(unit_price)
            FROM
            	transactions
            GROUP BY
                stock_code
            ''')
        conn.commit()
        conn.close()
        print('data succesfully loaded ✅')
        return
    except Exception as e:
        print("An error occured !!!"+ "\n" f"{e}")
        print("\n"+ f"exception type {type(e)}")
        return
        conn.close()
        
def main():
    #read data into dataframe
    df = pd.read_excel("C:/Users/Lenovo/Documents/MerchantOfVenice/Online Retail.xlsx")
    #making a copy of the data
    df0 = df.copy()
    
    #remove rows without customerID
    df0['CustomerID'].isnull().sum()
    df1 = df0[df0['CustomerID'].notnull()]
    
    #remove negative prices
    df1 = df1[df1['UnitPrice'] > 0]
    
    #remove negative quantity
    df1 = df1[df1['Quantity'] > 0]
    
    print(f"{len(df0) -len(df1)} rows have been removed")
    #drop duplicate values
    df2 = df1.drop_duplicates(subset=['InvoiceNo', 'StockCode', 'CustomerID'])
    print(f"{len(df1)-len(df2)} duplicate values removed")

    load_transcations(df1)
    load_customers()
    load_products()

main()
