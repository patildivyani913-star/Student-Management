from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# -----------------------------
# Database Connection Function
# -----------------------------
def connect_db():
    connection = sqlite3.connect("students.db")
    connection.row_factory = sqlite3.Row
    return connection


# -----------------------------
# Create Students Table
# -----------------------------
def create_table():
    connection = connect_db()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS students(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT,

            age INTEGER,

            course TEXT,

            city TEXT

        )
    """)

    connection.commit()
    connection.close()


create_table()


# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# Add Student
# -----------------------------
@app.route("/add", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        course = request.form["course"]
        city = request.form["city"]

        connection = connect_db()

        connection.execute(
            "INSERT INTO students(name, age, course, city) VALUES (?, ?, ?, ?)",
            (name, age, course, city)
        )

        connection.commit()
        connection.close()

        return redirect(url_for("view_students"))

    return render_template("addStudent.html")


# -----------------------------
# View Students
# -----------------------------
@app.route("/students")
def view_students():

    connection = connect_db()

    students = connection.execute(
        "SELECT * FROM students"
    ).fetchall()

    connection.close()

    return render_template(
        "viewStudents.html",
        students=students
    )


# -----------------------------
# Update Student
# -----------------------------
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update_student(id):

    connection = connect_db()

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        course = request.form["course"]
        city = request.form["city"]

        connection.execute(
            """
            UPDATE students
            SET
                name=?,
                age=?,
                course=?,
                city=?
            WHERE id=?
            """,
            (name, age, course, city, id)
        )

        connection.commit()
        connection.close()

        return redirect(url_for("view_students"))

    student = connection.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    ).fetchone()

    connection.close()

    return render_template(
        "updateStudent.html",
        student=student
    )


# -----------------------------
# Delete Student
# -----------------------------
@app.route("/delete/<int:id>")
def delete_student(id):

    connection = connect_db()

    connection.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("view_students"))


# -----------------------------
# Run Flask App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)