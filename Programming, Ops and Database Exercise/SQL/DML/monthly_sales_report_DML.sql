SELECT
MONTH(order_date) AS "month",
COUNT(DISTINCT order_id) AS total_number_of_orders,
sum(total_amount) AS total_monthly_sales
FROM greyshop.orders_aggregate
WHERE status in ('Shipped','Delivered')
GROUP BY 1
