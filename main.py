import os
from flask import Flask, jsonify
import oracledb

app = Flask(__name__)

# Fetch database credentials securely from Environment Variables
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_DSN = os.environ.get("DB_DSN")  # Connection string copied from Oracle Cloud

def get_db_data():
    # python-oracledb default thin mode works walletless over TLS
    with oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN) as connection:
        with connection.cursor() as cursor:
            # Replace with your actual table name
            cursor.execute("SELECT 'Hello from Autonomous DB!' FROM dual")
            result = cursor.fetchone()
            return result[0] if result else "No data"

@app.route("/")
def home():
    try:
        data = get_db_data()
        print(f"Fetched data from Oracle DB: {data}", flush=True)
        return jsonify({"status": "success", "data": data})
    except Exception as e:
        print(f"Database connection error: {e}", flush=True)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
