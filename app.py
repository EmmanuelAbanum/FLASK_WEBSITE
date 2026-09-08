import sqlite3
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from functools import wraps



app = Flask(__name__)
app.secret_key = "mysecretkey"


def login_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if "user" not in session:
            return redirect("/login")

        return function(*args, **kwargs)

    return wrapper


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

@app.route("/team")
def team():
    return render_template("team.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        conn = sqlite3.connect("database.db")

        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO messages(name,email,message) VALUES(?,?,?)",
            (name, email, message)
        )

        conn.commit()
        conn.close()

    return render_template("contact.html")


# @app.route("/login", methods=["GET", "POST"])
# def login():

#     if request.method == "POST":

#         username = request.form["username"]
#         password = request.form["password"]
# ###############################################        ###############################

#         conn = sqlite3.connect("database.db")

#         cursor = conn.cursor()

#         cursor.execute(
#             """
#             SELECT *
#             FROM users
#             WHERE username=?
#             AND password=?
#             """,
#             (username, password)
#         )

#         user = cursor.fetchone()

#         conn.close()

#         if user:

#             session["user"] = username

#             return redirect("/dashboard")
        
# #######################################################################
#             session["user"] = username

#             return redirect("/dashboard")

#     return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE username = ?
            """,
            (username,)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            if check_password_hash(user[2], password):

                session["user"] = username

                return redirect("/dashboard")

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():

    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM messages"
    )

    messages = cursor.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        messages=messages
    )

@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        ##########
        password = generate_password_hash(
            request.form["password"]
        )
        #########

        conn = sqlite3.connect("database.db")

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users(
                username,
                password
            )
            VALUES(?,?)
            """,
            (username, password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)