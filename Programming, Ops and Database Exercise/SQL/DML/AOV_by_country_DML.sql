SELECT 
sum(total_amount) AS total_sales,
count(order_id) AS total_orders,
sum(total_amount) / count(order_id) as aov
FROM greyshop.orders_aggregate
