from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import os
import time

app = Flask(__name__)
app.secret_key = "student-management-secret"


# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "root123"),
        database=os.getenv("DB_NAME", "student_db")
    )


# Create database table
def initialize_database():
    for attempt in range(15):
        try:
            db = get_db_connection()
            cursor = db.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    roll_number VARCHAR(20) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    course VARCHAR(50) NOT NULL
                )
            """)

            db.commit()
            cursor.close()
            db.close()

            print("Database connected successfully!")
            return

        except mysql.connector.Error as error:
            print(f"Database connection attempt {attempt + 1}: {error}")
            time.sleep(3)

    raise RuntimeError("Could not connect to MySQL database.")


# Home page - Display students
@app.route("/")
def index():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students ORDER BY id DESC")
    students = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("index.html", students=students)


# Add or update student
@app.route("/save", methods=["POST"])
def save_student():

    student_id = request.form.get("id")
    name = request.form["name"].strip()
    roll_number = request.form["roll_number"].strip()
    email = request.form["email"].strip()
    course = request.form["course"].strip()

    if not all([name, roll_number, email, course]):
        flash("Please fill in all fields.")
        return redirect(url_for("index"))

    db = get_db_connection()
    cursor = db.cursor()

    if student_id:
        cursor.execute("""
            UPDATE students
            SET name=%s, roll_number=%s, email=%s, course=%s
            WHERE id=%s
        """, (name, roll_number, email, course, student_id))

        flash("Student updated successfully!")

    else:
        cursor.execute("""
            INSERT INTO students
            (name, roll_number, email, course)
            VALUES (%s, %s, %s, %s)
        """, (name, roll_number, email, course))

        flash("Student added successfully!")

    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for("index"))


# Delete student
@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=%s",
        (student_id,)
    )

    db.commit()
    cursor.close()
    db.close()

    flash("Student deleted successfully!")

    return redirect(url_for("index"))


# Start application
if __name__ == "__main__":
    initialize_database()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )