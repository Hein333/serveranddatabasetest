import os
from flask import Flask, jsonify
import oracledb

app = Flask(__name__)

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_DSN = os.environ.get("DB_DSN")

@app.route("/")
def home():
    try:
        with oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN) as connection:
            with connection.cursor() as cursor:
                
                # --- CHANGE THIS LINE to your actual table name ---
                cursor.execute("SELECT * FROM students")
                
                # Fetch all rows from your table
                rows = cursor.fetchall()
                
                # Get the column names so your JSON looks organized
                columns = [col[0] for col in cursor.description]
                
                # Combine column names and row data into a list of dictionaries
                results = [dict(zip(columns, row)) for row in rows]
                
                print(f"Successfully fetched {len(results)} rows from database.", flush=True)
                return jsonify({"status": "success", "row_count": len(results), "data": results})
                
    except Exception as e:
        print(f"Database query error: {e}", flush=True)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
