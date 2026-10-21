import os
from flask import Flask, render_template,request
import oracledb

app = Flask(__name__)

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_DSN = os.environ.get("DB_DSN")

@app.route("/FRUITS")
def fruits():
    try:
        with oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN) as connection:
            with connection.cursor() as cursor:
                # --- CHANGE THIS to your actual table name ---
                cursor.execute("SELECT * FROM sheet1")
                
                rows = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                print(rows)
                print(rows[0])
                print(f"Successfully fetched {len(rows)} rows from database.", flush=True)
                return render_template("index.html", columns=columns, rows=rows)
                
    except Exception as e:
        print(f"Database query error: {e}", flush=True)
        return render_template("index.html", error=str(e))


@app.route("/student")
def student():
    try:
        with oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN) as connection:
            with connection.cursor() as cursor:
                # --- CHANGE THIS to your actual table name ---
                cursor.execute("SELECT * FROM students")
                
                rows = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                
                print(f"Successfully fetched {len(rows)} rows from database.", flush=True)
                return render_template("index.html", columns=columns, rows=rows)
                
    except Exception as e:
        print(f"Database query error: {e}", flush=True)
        return render_template("index.html", error=str(e))


@app.route("/")
def home():
    try:
        with oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN) as connection:
            with connection.cursor() as cursor:
                # --- CHANGE THIS to your actual table name ---
                cursor.execute("SELECT * FROM sheet1")
                
                rows = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                print(f"Successfully fetched {len(rows)} rows from database.", flush=True)
                return render_template("home.html", columns=columns, rows=rows)
                
    except Exception as e:
        print(f"Database query error: {e}", flush=True)
        return render_template("home.html", error=str(e))


@app.route("/submit",methods=["post"])
def submit():
    firstname = request.form.get('first_name')
    lastname = request.form.get('last_name')
    try:
        with oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN) as connection:
            with connection.cursor() as cursor:
                # --- CHANGE THIS to your actual table name ---
                # Using positional placeholders (:1, :2)
                sql = "INSERT INTO cusdata (gmail,password) VALUES (:1, :2)"
                cursor.execute(sql, (firstname, lastname))
                connection.commit()
                
                return 'successfully updated'
    except Exception as e:
        print(f"Database query error: {e}", flush=True)
        return render_template("index.html", error=str(e))

@app.route("/login",methods=["post"])
def submit():
    firstname = request.form.get('first_name')
    lastname = request.form.get('last_name')
    try:
        with oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM cusdata")
                
                rows = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                print(rows)
                
                return 'successfully logged IN'
    except Exception as e:
        print(f"Database query error: {e}", flush=True)
        return render_template("index.html", error=str(e))

    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
