"""
RFM Customer Segmentation
"""
import pyodbc

def create_rfm_segmentation():
    """Execute RFM segmentation and create customer_segments table"""
    
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=YOUR_SERVER;'
        'DATABASE=MerchantOfVenice;'
        'Trusted_Connection=yes;'
    )
    
    cursor = conn.cursor()
    
    # Drop existing table if exists
    cursor.execute("DROP TABLE IF EXISTS customer_segments")
    
    # Execute segmentation query
    segmentation_sql = """
    WITH rfm_calc AS (
        SELECT 
            customer_id,
            DATEDIFF(day, MAX(invoice_date), '2011-12-09') as recency_days,
            COUNT(DISTINCT invoice_no) as frequency,
            SUM(quantity * unit_price) as monetary
        FROM transactions
        GROUP BY customer_id
    ),
    rfm_scores AS (
        SELECT
	*,
	CASE
		WHEN NTILE(5) OVER(ORDER BY recency_days) = 1 THEN 5
		WHEN NTILE(5) OVER(ORDER BY recency_days) = 2 THEN 4
		WHEN NTILE(5) OVER(ORDER BY recency_days) = 3 THEN 3
		WHEN NTILE(5) OVER(ORDER BY recency_days) = 4 THEN 2
		else 1
	END R,
	NTILE(5) OVER(ORDER BY frequency ASC) [F],
	NTILE(5) OVER(ORDER BY monetary ASC) [M]
FROM
	rfm_table)
,rfm_segments AS
(SELECT
	*,
	CAST(r as VARCHAR) + CAST(f AS VARCHAR) + CAST(m AS varchar) [rfm score],
	-- Segment classification
        CASE
            -- Champions: Best customers
            WHEN R >= 4 AND F >= 4 AND M >= 4 THEN 'Champions'
            
            -- Loyal: Buy frequently
            WHEN F >= 4 THEN 'Loyal'
            
            -- Big Spenders: High monetary value
            WHEN M >= 4 THEN 'Big Spenders'
            
            -- At Risk: Were good, now declining
            WHEN R <= 2 AND F >= 3 THEN 'At Risk'
            
            -- Lost: Haven't bought recently
            WHEN R <= 2 AND F <= 2 THEN 'Lost'
			-- Promising: Recent but low frequency/monetary
            WHEN R >= 4 AND F <= 2 THEN 'Promising'
            
            -- Need Attention: Mid-range, could go either way
            WHEN R = 3 AND F = 3 THEN 'Need Attention'
			ELSE 'Others'
        END as segment
FROM
	rfm_scores
    )
    SELECT *
    INTO customer_segments
    FROM rfm_segments
    """
    
    cursor.execute(segmentation_sql)
    conn.commit()
    
    # Verify
    cursor.execute("SELECT COUNT(*) FROM customer_segments")
    count = cursor.fetchone()[0]
    print(f"✅ Segmentation complete! {count} customers segmented")
    
    # Show summary
    cursor.execute("""
        SELECT segment, COUNT(*) as count
        FROM customer_segments
        GROUP BY segment
        ORDER BY count DESC
    """)
    
    print("\nSegment Summary:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} customers")
    
    conn.close()

if __name__ == "__main__":
    create_rfm_segmentation()
