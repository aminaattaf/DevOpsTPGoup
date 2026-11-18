import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "teamdb"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres")
    )


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id SERIAL PRIMARY KEY,
            nom VARCHAR(100) NOT NULL,
            prenom VARCHAR(100) NOT NULL,
            email VARCHAR(150) UNIQUE NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "environment": os.getenv("APP_ENV", "dev")
    }), 200


@app.route("/api/members", methods=["GET"])
def get_members():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, nom, prenom, email FROM members ORDER BY id ASC;")
    members = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(members), 200


@app.route("/api/members", methods=["POST"])
def add_member():
    data = request.form
 
    if not all(data.get(k) for k in ("nom", "prenom", "email")):
        return "Nom, prénom et email requis", 400
 
    conn = get_db_connection()
    cur = conn.cursor()
 
    try:
        cur.execute(
            "INSERT INTO members (nom, prenom, email) VALUES (%s, %s, %s)",
            (data["nom"], data["prenom"], data["email"])
        )
        conn.commit()
        return "Inscription enregistrée !", 201
 
    except psycopg2.IntegrityError:
        conn.rollback()
        return "Cet email existe déjà", 409
 
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)