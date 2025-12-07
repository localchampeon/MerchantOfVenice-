--use MerchantOfVenice;

WITH rfm_table AS
(SELECT
	customer_id,
	DATEDIFf(day, MAX(invoice_date), '2011-12-09') [recency_days],
	COUNT(invoice_no) [frequency],
	SUM(quantity * unit_price) [monetary]
FROM
	transactions
GROUP BY
	customer_id)
, rfm_scores AS
(SELECT
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
	rfm_scores)
SELECT *
INTO customer_segments
FROM rfm_segments; -- save to table

SELECT 
    segment,
    COUNT(*) as customer_count,
    CAST(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS DECIMAL(5,2)) as percentage,
    AVG(recency_days) as avg_recency,
    AVG(frequency) as avg_frequency,
    AVG(monetary) as avg_monetary
FROM rfm_segments
GROUP BY segment
ORDER BY customer_count DESC

last updated 2025-12-07
