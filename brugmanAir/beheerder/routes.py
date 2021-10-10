from itertools import count
from flask import render_template, redirect, flash, url_for, session, logging, request, jsonify
from functools import wraps
from passlib.hash import sha256_crypt
from brugmanAir import app, mysql
from brugmanAir.beheerder.forms import RegisterForm
from uuid import uuid4


# chech if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash(f"Unauthorized, please login", "danger")
            return redirect(url_for("login"))
    return wrap


def is_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session and "admin" in session:
            return f(*args, **kwargs)
        else:
            flash(f"Unauthorized, only admins are allowed to view this page", "danger")
            return redirect(url_for("login"))
    return wrap

def rows_num(table_name):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM {table_name}")
    result_len = len(cur.fetchall())

    cur.close()
    return result_len


def get_data(table_name):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM {table_name}")
    result_data = cur.fetchall()

    return result_data


def get_data_con(table_name, where, row):
    cur = mysql.connection.cursor()
    cur.execute(
        f"SELECT * FROM {table_name} WHERE {row} = %s", [where])
    result_data = cur.fetchall()

    return result_data


def get_one(table_name, where, row):
    cur = mysql.connection.cursor()
    cur.execute(
        f"SELECT * FROM {table_name} WHERE {row} = %s", [where])
    result_data = cur.fetchone()

    return result_data


def get_one_cell(table_name, where, row, cell):
    cur = mysql.connection.cursor()
    cur.execute(
        f"SELECT {cell} FROM {table_name} WHERE {row} = %s", [where])
    result_data = cur.fetchone()

    return result_data


def get_all_cell(table_name, cell):
    cur = mysql.connection.cursor()
    cur.execute(
        f"SELECT {cell} FROM {table_name}")
    result_data = cur.fetchall()

    return result_data


def get_piloot_co(positie, id):
    cur = mysql.connection.cursor()
    cur.execute(
        f"""SELECT medewerker.voornaam 
                FROM medewerker 
                INNER JOIN vlucht_medewerker 
                WHERE medewerker.id = vlucht_medewerker.medewerker_id 
                AND medewerker.positie = '{positie}'
                AND vlucht_medewerker.vlucht_id =%s""", [id])
    data = cur.fetchone()
    return data


@app.route("/")
@app.route("/home")
def home():
    return render_template("admin/index.html", title="home")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    cur = mysql.connection.cursor()

    if request.method == "POST" and form.validate():
        beheerder_id = uuid4().hex
        fname = form.fname.data
        lname = form.lname.data
        gender = request.form["gender"]
        straatnaam = form.straatnaam.data
        huisnr = form.huisnr.data
        postcode = form.postcode.data
        plaats = form.plaats.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))

        existing_user = cur.execute(
            "SELECT * FROM beheerder WHERE email = %s", [email])

        if existing_user > 0:
            flash("This email is already used", "danger")

            return redirect(url_for("register"))
        else:
            sql = "INSERT INTO beheerder VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql, (beheerder_id, fname, lname, email, straatnaam,
                              huisnr, postcode, plaats, gender, password))
            mysql.connection.commit()
            flash("Registered successfully", "success")

            return redirect(url_for("login"))

    cur.close()

    return render_template("admin/register.html", title="register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.values["email"]
        password_can = request.values["passowrd"]

        cur = mysql.connection.cursor()

        result = cur.execute(
            "SELECT * FROM beheerder WHERE email = %s ", [email])

        if result > 0:
            data = cur.fetchone()
            password = data["wachtwoord"]
            fname = data["voornaam"]
            lname = data["achternaam"]

            if sha256_crypt.verify(password_can, password):
                session["logged_in"] = True
                session.permanent = False
                session["fname"] = fname[0].upper()
                session["lname"] = lname[0].upper()
                session["name"] = fname
                session["id"] = data["id"]

                flash("you re now logged in successfully", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("invalid email or password", "danger")
        else:
            flash("No user found", "danger")

        cur.close()

    return render_template("admin/login.html", title="login")

@app.route("/dashboard")
@is_logged_in
def dashboard():
    cur = mysql.connection.cursor()

    piloten_len = rows_num("medewerker")
    bestemmingen_len = rows_num("bestemming")
    vliegtuigen_len = rows_num("vliegtuig")
    vluchten_len = rows_num("vlucht")

    medewerker = get_data("medewerker")
    vluchten_data = get_data("vlucht")
    bestemmingen_data = get_data("bestemming")
    vliegtuigen_data = get_data("vliegtuig")

    vertrek_locaties = []

    for vlucht in vluchten_data:
        vertrek = get_one_cell(
            "bestemming", vlucht["vertrek_locatie"], "id", "stad")
        bestemming = get_one_cell(
            "bestemming", vlucht["Bestemming_id"], "id", "stad")

        vlucht["vertrek_locatie"] = vertrek["stad"]
        vlucht["Bestemming_id"] = bestemming["stad"]

        piloot = get_piloot_co("piloot", vlucht["id"])
        co_piloot = get_piloot_co("co-piloot", vlucht["id"])
        vlucht["piloot"] = piloot["voornaam"]
        vlucht["co_piloot"] = co_piloot["voornaam"]

    return render_template("admin/dashboard.html", title="Dashboard", vluchten_len=vluchten_len, vluchten_data=vluchten_data,
                           bestemmingen_len=bestemmingen_len, bestemmingen_data=bestemmingen_data,
                           data=medewerker, piloten_len=piloten_len, vliegtuigen_len=vliegtuigen_len, vertrek_locaties=vertrek_locaties, vliegtuigen_data=vliegtuigen_data)


@app.route("/logout")
def logout():
    session.clear()
    flash("you are logged out", "success")
    return redirect(url_for("login"))


@app.errorhandler(404)
def not_found(e):
    return render_template("not_found.html")

