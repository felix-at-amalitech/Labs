SELECT
customer_id,
sum(total_amount) AS customer_money_spent
FROM greyshop.orders_aggregate
WHERE status != 'cancelled'
-- AND MONTH(order_date) in (11)
GROUP BY 1
ORDER BY customer_money_spent DESC
LIMIT 1