
SELECT 
customer_id,
count(order_id) AS total_orders
FROM greyshop.orders_aggregate
GROUP BY 1
HAVING count(order_id) > 1
