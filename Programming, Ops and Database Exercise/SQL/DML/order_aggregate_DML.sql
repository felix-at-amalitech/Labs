INSERT INTO greyshop.orders_aggregate(order_id, customer_id, order_date, status, country, total_amount)
WITH order_price as (
SELECT
order_id,
quantity * unit_price as order_total_price
FROM 
greyshop.order_items
),
order_aggregate_cte as (
SELECT 
o.order_id,
o.customer_id,
o.order_date,
o.status,
op.order_total_price as total_price
FROM greyshop.orders o
LEFT JOIN order_price op
ON o.order_id = op.order_id
),
order_aggregate_with_country as (
  SELECT
    o.order_id,
    o.customer_id,
    o.order_date,
    o.status,
    o.total_price,
    c.country
  FROM order_aggregate_cte o
  LEFT JOIN greyshop.customers c
  ON o.customer_id = c.customer_id
)
SELECT
order_id,
customer_id,
order_date,
status,
country,
sum(total_price) AS total_amount
FROM order_aggregate_with_country
GROUP BY 1,2,3
