INSERT INTO greyshop.product_inventory(product_id, quantity_sold, category, quantity_available, unit_price)
WITH order_item_count AS (
SELECT 
product_id,
sum(quantity) AS quantity_ordered
FROM greyshop.order_items
GROUP BY 1
),
product_inventory AS (
SELECT 
p.product_id,
coalesce(oi.quantity_ordered, 0) AS quantity_sold,
category,
price AS unit_price
FROM greyshop.products p
LEFT JOIN order_item_count oi 
ON p.product_id = oi.product_id 
)
SELECT
product_id,
quantity_sold,
category,
10 AS quantity_available,
unit_price
FROM product_inventory 

