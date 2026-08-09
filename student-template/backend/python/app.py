from flask import Flask, jsonify
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")


@app.route('/api/inventory/alerts', methods=['GET'])
def get_alerts():
    """
    Return all inventory products where quantity <= reorder_level.
    """
    conn = None

    try:
        conn = psycopg2.connect(DATABASE_URL)

        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT id, product_name, quantity, reorder_level
                FROM inventory
                WHERE quantity <= reorder_level
            """)

            alerts = cursor.fetchall()

        return jsonify(alerts), 200

    except Exception as e:
        app.logger.error("Failed to fetch inventory alerts: %s", e)
        return jsonify({"error": "Failed to fetch inventory alerts"}), 500

    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
