from flask import Flask, jsonify, request
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv()

# --- Database Configuration ---
# Load configuration from environment variables
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_DATABASE'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'port': os.getenv('DB_PORT', 3306)
}

# --- Database Connection Helper ---
def get_db_connection():
    """Establishes a connection to the database."""
    try:
        print(db_config.items())
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None



# --- API Endpoints ---
@app.route('/')
def index():
    """Root endpoint."""
    return "Welcome to GREYSHOP Reports API!"

@app.route('/reports/top_customers', methods=['GET'])
def get_top_customers():
    """
    Endpoint to get top customers by total spending from the database.

    Optional Query Parameters:
        - limit (int): The maximum number of top customers to return. Defaults to 10.
    """
    limit = request.args.get('limit', default=1, type=int)
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True) # Use dictionary=True to get column names
    top_customers_list = []

    try:
        query = """
        SELECT
        customer_id,
        sum(total_amount) AS customer_money_spent
        FROM greyshop.orders_aggregate
        WHERE status != 'cancelled'
        GROUP BY customer_id
        ORDER BY customer_money_spent DESC
        LIMIT %s;
        """
        cursor.execute(query, (limit,))
        top_customers_list = cursor.fetchall()

    except Error as e:
        print(f"Error executing query for top customers: {e}")
        return jsonify({"error": "Failed to retrieve top customers"}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    # Ensure decimal values are floats for JSON serialization
    for customer in top_customers_list:
         customer['customer_money_spent'] = float(customer['customer_money_spent'])


    return jsonify(top_customers_list)

@app.route('/reports/monthly_sales', methods=['GET'])
def get_monthly_sales():
    """
    Endpoint to get monthly sales reports for Shipped and Delivered orders from the database.
    """
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)
    monthly_sales_list = []

    try:
        query = """
          SELECT
          MONTH(order_date) AS "month",
          COUNT(DISTINCT order_id) AS total_number_of_orders,
          sum(total_amount) AS total_monthly_sales
          FROM greyshop.orders_aggregate
          WHERE status in ('Shipped','Delivered')
          GROUP BY 1
        """
        cursor.execute(query)
        monthly_sales_list = cursor.fetchall()

    except Error as e:
        print(f"Error executing query for monthly sales: {e}")
        return jsonify({"error": "Failed to retrieve monthly sales"}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    # Ensure decimal values are floats for JSON serialization
    for month_data in monthly_sales_list:
         month_data['total_monthly_sales'] = float(month_data['total_monthly_sales'])

    return jsonify(monthly_sales_list)

@app.route('/reports/products_never_ordered', methods=['GET'])
def get_products_never_ordered():
    """
    Endpoint to list products that have never been included in any order items from the database.
    """
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)
    never_ordered_products_list = []

    try:
        query = """
          SELECT
          *
          FROM greyshop.product_inventory
          WHERE quantity_sold = 0
        """
        cursor.execute(query)
        never_ordered_products_list = cursor.fetchall()

    except Error as e:
        print(f"Error executing query for products never ordered: {e}")
        return jsonify({"error": "Failed to retrieve products never ordered"}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return jsonify(never_ordered_products_list)

@app.route('/reports/aov_by_country', methods=['GET'])
def get_aov_by_country():
    """
    Endpoint to calculate Average Order Value (AOV) grouped by customer country from the database.
    Includes all orders, regardless of status.
    """
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)
    aov_list = []

    try:
        query = """
          SELECT
          country,
          sum(total_amount) AS total_sales,
          count(order_id) AS total_orders,
          sum(total_amount) / count(order_id) as aov
          FROM greyshop.orders_aggregate
          GROUP BY country
        """
        cursor.execute(query)
        aov_list = cursor.fetchall()

    except Error as e:
        print(f"Error executing query for AOV by country: {e}")
        return jsonify({"error": "Failed to retrieve AOV by country"}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    # Ensure decimal values are floats for JSON serialization
    for country_data in aov_list:
         country_data['aov'] = float(country_data['aov'])
         country_data['total_sales'] = float(country_data['total_sales'])


    return jsonify(aov_list)


@app.route('/reports/frequent_buyers', methods=['GET'])
def get_frequent_buyers():
    """
    Endpoint to list customers who have placed more than one order from the database.
    """
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)
    frequent_buyers_list = []

    try:
        query = """
            SELECT 
            customer_id,
            count(order_id) AS total_orders
            FROM greyshop.orders_aggregate
            GROUP BY 1
            HAVING count(order_id) > 1
        """
        cursor.execute(query)
        frequent_buyers_list = cursor.fetchall()

    except Error as e:
        print(f"Error executing query for frequent buyers: {e}")
        return jsonify({"error": "Failed to retrieve frequent buyers"}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return jsonify(frequent_buyers_list)


# --- Run the App ---
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    