DROP TABLE IF EXISTS orders_aggregate;

CREATE TABLE IF NOT EXISTS orders_aggregate (
    order_id INT NOT NULL,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL,
    country VARCHAR(50) NOT NULL,
    total_amount DECIMAL(42, 2) NOT NULL,
    PRIMARY KEY (order_id)
);