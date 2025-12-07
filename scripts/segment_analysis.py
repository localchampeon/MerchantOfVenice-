"""
Analyze customer segments
"""
import pyodbc
import pandas as pd

conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=YOUR_SERVER;'
    'DATABASE=MerchantOfVenice;'
    'Trusted_Connection=yes;'
)

# Segment summary
query = """
SELECT 
    segment,
    COUNT(*) as customers,
    AVG(monetary) as avg_spent,
    SUM(monetary) as total_revenue
FROM customer_segments
GROUP BY segment
ORDER BY total_revenue DESC
"""

df = pd.read_sql(query, conn)
print("CUSTOMER SEGMENTS:")
print(df)

conn.close()
