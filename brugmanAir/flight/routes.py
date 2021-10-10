from itertools import zip_longest
from flask import json, render_template, redirect, flash, url_for, session, request
from brugmanAir import app, mysql
from brugmanAir.flight.forms import Medewerker, Bestemming, Plane
from uuid import uuid4
from brugmanAir.beheerder.routes import is_logged_in, get_one, get_data_con, get_data, get_one_cell, rows_num


def get_medewerkers(positie, flight_id):
    cur = mysql.connection.cursor()
    piloten_list = []

    cur.execute(
        """SELECT medewerker.voornaam
                FROM medewerker
                INNER JOIN vlucht_medewerker
                WHERE medewerker.id = vlucht_medewerker.medewerker_id
                AND medewerker.positie =%s
                AND vlucht_medewerker.vlucht_id =%s""", [positie, flight_id])
    piloten_data = cur.fetchall()

    for indx, piloot in enumerate(piloten_data):
        piloten_list.append(piloot["voornaam"])

    return piloten_list


def update_medewerker(positie, flight_id, oud):
    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE vlucht_medewerker SET medewerker_id=%s WHERE Vlucht_id=%s AND Medewerker_id=%s", [positie, flight_id, oud])

    mysql.connection.commit()
    cur.close()


@app.route('/new-flight', methods=['POST', 'GET'])
@is_logged_in
def new_flight():
    piloten = get_data_con("medewerker", "piloot", "positie")
    co_piloten = get_data_con("medewerker", "co-piloot", "positie")
    stewards = get_data_con("medewerker", "steward", "positie")
    vliegtuigen = get_data("vliegtuig")
    bestemmingen = get_data("bestemming")

    cur = mysql.connection.cursor()
    if request.method == "POST":
        flight = request.get_json()
        if flight:
            medewerkers = []

            vlucht_id = uuid4().hex
            beheerder_id = session["id"]
            medewerkers.append(get_one_cell(
                "medewerker", flight["pilo1"], "voornaam", "id")["id"])
            medewerkers.append(get_one_cell(
                "medewerker", flight["co_pil"], "voornaam", "id")["id"])
            medewerkers.append(get_one_cell(
                "medewerker", flight["stew1"], "voornaam", "id")["id"])
            medewerkers.append(get_one_cell(
                "medewerker", flight["stew2"], "voornaam", "id")["id"])
            bestemming_id = get_one_cell(
                "bestemming", flight["bestemming"], "stad", "id")["id"]
            vliegtuig_id = flight["vliegtuig"]
            vertrek = get_one_cell(
                "bestemming", flight["vertrek"], "stad", "id")["id"]

            datum = flight["datum"]
            vertrektijd = flight["vertrektijd"]
            aankomsttijd = flight["aankomsttijd"]
            prijs = flight["prijs"]

            sql = "INSERT INTO vlucht VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql, [vlucht_id, datum, vertrektijd, aankomsttijd,
                        vertrek, prijs, bestemming_id, vliegtuig_id, beheerder_id])

            for medewerker_id in medewerkers:
                cur.execute("INSERT INTO vlucht_medewerker VALUES(%s,%s)",
                            [vlucht_id, medewerker_id])

            mysql.connection.commit()
            cur.close()

        flash("Nieuwe vlucht is toegevoegd", "success")
        return redirect(url_for("new_flight"))

    return render_template("flight/add/new_flight.html", title="Vlucht", overview_title="Nieuwe Vlucht", icon_name="flight", css_icon="flight-icon", piloten=piloten, stewards=stewards, vliegtuigen=vliegtuigen, bestemmingen=bestemmingen, btn_name="Toevoegen", co_piloten=co_piloten)


@app.route('/new-des', methods=['POST', 'GET'])
@is_logged_in
def new_des():
    form = Bestemming(request.form)
    cur = mysql.connection.cursor()

    if request.method == "POST" and form.validate_on_submit():
        des_id = uuid4().hex
        land = form.land.data
        stad = form.stad.data
        luchthaven = form.luchthaven.data
        beheerder_id = session["id"]

        result = cur.execute(
            "SELECT * FROM bestemming WHERE luchthaven = %s", [luchthaven])

        if result > 0:
            flash("Deze luchthaven is al toegevoegd", "danger")
            return redirect(url_for("new_des"))
        else:
            cur.execute("INSERT INTO bestemming VALUES(%s,%s,%s,%s,%s)", [
                        des_id, stad, land, luchthaven, beheerder_id])
            flash("luchthaven is toegevoegd", "success")

            mysql.connection.commit()
            return redirect(url_for("new_des"))

    cur.close()

    return render_template("flight/add/new_des.html", title="Bestemming", form=form, overview_title="Nieuwe Bestemming", icon_name="place", css_icon="place-icon")


@app.route('/new-mwerker', methods=['POST', 'GET'])
@is_logged_in
def new_crew():
    form = Medewerker(request.form)
    cur = mysql.connection.cursor()

    if request.method == "POST" and form.validate_on_submit():
        crew_id = uuid4().hex
        fname = form.fname.data
        lname = form.lname.data
        email = form.email.data
        postcode = form.postcode.data
        gender = request.form["gender"]
        positie = request.form["positie"]

        existing_user = cur.execute(
            "SELECT * FROM medewerker WHERE email = %s", [email])

        if existing_user > 0:
            flash("This medewerker is al toegevoegd", "danger")
            return redirect(url_for("new_crew"))

        else:
            sql = "INSERT INTO medewerker VALUES(%s,%s,%s,%s,%s,%s,%s)"

            cur.execute(sql, [crew_id, fname, lname,
                        postcode, positie, gender, email])
            mysql.connection.commit()
            flash("Medewerker is toegevoegd", "success")

            return redirect(url_for("new_crew"))

    return render_template("flight/add/new_mwerker.html", title="Medewerker", form=form, overview_title="Nieuwe Medewerker", icon_name="person_add", css_icon="crew-icon")


@app.route("/new-plane", methods=['POST', 'GET'])
@is_logged_in
def new_plane():
    form = Plane(request.form)
    cur = mysql.connection.cursor()

    vliegtuigen_len = rows_num("vliegtuig")

    if request.method == "POST" and form.validate_on_submit():
        vliegtuig_id = f"BA-{vliegtuigen_len+1}"
        spanwijdte = form.spanwijdte.data
        lengte = form.lengte.data
        hoogte = form.hoogte.data
        gewicht = form.gewicht.data
        snelheid = form.snelheid.data
        bereik = form.bereik.data
        aantal = form.aantal.data
        locatie = form.locatie.data
        beheerder_id = session["id"]

        sql = "INSERT INTO vliegtuig(id, spanwijdte, lengte, hoogte, gewicht_bij_vertrek, kruissnelheid, bereik, aantal_passagiers, Beheerder_id, locatie) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        cur.execute(sql, [vliegtuig_id, spanwijdte, lengte, hoogte,
                    gewicht, snelheid, bereik, aantal, beheerder_id, locatie])

        mysql.connection.commit()
        cur.close()

        flash("vliegtuig is toegvoegd", "success")
        return redirect(url_for("new_plane"))

    return render_template("flight/add/new_plane.html", title="Vliegtuig", form=form, overview_title="Nieuw Vliegtuig", icon_name="flight", css_icon="plane-icon")


@app.route("/delete-vlucht", methods=['POST', 'GET'])
@is_logged_in
def delete_vlucht():
    cur = mysql.connection.cursor()
    get_data = request.get_json(force=True)

    for id in get_data:
        cur.execute("DELETE FROM vlucht WHERE id = %s", [id])

    mysql.connection.commit()
    cur.close()

    return redirect(url_for("dashboard"))


@app.route('/delete-dest', methods=['POST', 'GET'])
@is_logged_in
def delete_dest():
    cur = mysql.connection.cursor()
    get_data = request.get_json(force=True)

    for id in get_data:
        cur.execute("DELETE FROM bestemming WHERE id = %s", [id])

    mysql.connection.commit()
    cur.close()

    return redirect(url_for("dashboard"))


@app.route('/delete-crew', methods=['POST', 'GET'])
@is_logged_in
def delete_crew():
    cur = mysql.connection.cursor()
    get_data = request.get_json(force=True)

    for id in get_data:
        cur.execute("DELETE FROM medewerker WHERE id = %s", [id])

    mysql.connection.commit()
    cur.close()

    return redirect(url_for("dashboard"))


@app.route('/delete-plane', methods=['POST', 'GET'])
@is_logged_in
def delete_plane():
    cur = mysql.connection.cursor()
    get_data = request.get_json(force=True)

    for id in get_data:
        cur.execute("DELETE FROM vliegtuig WHERE id = %s", [id])

    mysql.connection.commit()
    cur.close()

    return redirect(url_for("dashboard"))


@app.route("/edit-flight/<flight_id>", methods=['POST', 'GET'])
@is_logged_in
def edit_vlucht(flight_id):
    piloten = get_data_con("medewerker", "piloot", "positie")
    co_piloten = get_data_con("medewerker", "co-piloot", "positie")
    stewards = get_data_con("medewerker", "steward", "positie")
    vliegtuigen = get_data("vliegtuig")
    bestemmingen = get_data("bestemming")

    vlucht = get_one("vlucht", flight_id, "id")
    bestemming = get_one_cell(
        "bestemming", vlucht["Bestemming_id"], "id", "stad")["stad"]
    vertrek_locatie = get_one_cell(
        "bestemming", vlucht["vertrek_locatie"], "id", "stad")["stad"]
    piloten_list = get_medewerkers('piloot', flight_id)
    stewards_list = get_medewerkers('steward', flight_id)
    co_piloten_list = get_medewerkers('co-piloot', flight_id)

    return render_template("flight/edit/edit_flight.html", title="Vlucht", overview_title="Wijzig Vlucht", icon_name="flight", css_icon="flight-icon", co_piloten=co_piloten, piloten=piloten, stewards=stewards, vliegtuigen=vliegtuigen, bestemmingen=bestemmingen, vertrekdatum=vlucht["vertrekdatum"], vertrektijd=vlucht["vertrektijd"], aankomsttijd=vlucht["aankomsttijd"], prijs=vlucht["prijs"], vliegtuig=vlucht["Vliegtuig_id"], vertrek_locatie=vertrek_locatie, bestemming=bestemming, piloot=piloten_list[0], co_piloot=co_piloten_list[0], steward1=stewards_list[0], steward2=stewards_list[1], flight_id=flight_id)


@app.route("/edit-flight/flight/<flight_id>", methods=['POST', 'GET'])
@is_logged_in
def edit_flight(flight_id):
    cur = mysql.connection.cursor()
    flight = request.get_json()

    if request.method == "POST" and flight != None:
        print(flight)
        medewerkers = []
        medewerkers.append(get_one_cell(
            "medewerker", flight["pilo1"], "voornaam", "id")["id"])
        medewerkers.append(get_one_cell(
            "medewerker", flight["co_pil"], "voornaam", "id")["id"])
        medewerkers.append(get_one_cell(
            "medewerker", flight["stew1"], "voornaam", "id")["id"])
        medewerkers.append(get_one_cell(
            "medewerker", flight["stew2"], "voornaam", "id")["id"])
        bestemming_id = get_one_cell(
            "bestemming", flight["bestemming"], "stad", "id")["id"]
        vliegtuig_id = flight["vliegtuig"]
        vertrek = get_one_cell(
            "bestemming", flight["vertrek"], "stad", "id")["id"]

        cur.execute("UPDATE vlucht SET vertrekdatum=%s, vertrektijd=%s, aankomsttijd=%s, vertrek_locatie=%s, prijs=%s, Bestemming_id=%s, Vliegtuig_id=%s WHERE id=%s", [
                    flight["datum"], flight["vertrektijd"], flight["aankomsttijd"], vertrek, flight["prijs"], bestemming_id, vliegtuig_id, flight_id])

        cur.execute(
            "DELETE FROM vlucht_medewerker WHERE Vlucht_id=%s", [flight_id])
        for medewerker_id in medewerkers:
            cur.execute("INSERT INTO vlucht_medewerker VALUES(%s,%s)",
                        [flight_id, medewerker_id])

        mysql.connection.commit()
        cur.close()

        return redirect(url_for("dashboard"))
    flash("Vlucht is gewijzigd", "success")
    return redirect(url_for("dashboard"))


@app.route('/edit-crew/<id>', methods=['POST', 'GET'])
@is_logged_in
def edit_crew(id):
    form = Medewerker(request.form)
    cur = mysql.connection.cursor()

    crew = get_one("medewerker", id, "id")
    form.fname.data = crew["voornaam"]
    form.lname.data = crew["achternaam"]
    form.postcode.data = crew["postcode"]
    form.email.data = crew["email"]

    if request.method == "POST" and form.validate_on_submit():
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]
        postcode = request.form["postcode"]

        sql = "UPDATE medewerker SET voornaam=%s, achternaam=%s, postcode=%s, email=%s WHERE id=%s"

        cur.execute(sql, (fname, lname, postcode, email, id))
        mysql.connection.commit()
        cur.close()
        flash("Medewerker is gewijzigd", "success")

        return redirect(url_for("dashboard"))

    return render_template("flight/edit/edit_mwerker.html", title="Medewerker", form=form, overview_title="Wijzig Medewerker", icon_name="person_add", css_icon="crew-icon")


@app.route('/edit-dest/<string:id>', methods=['POST', 'GET'])
@is_logged_in
def edit_dest(id):
    form = Bestemming(request.form)
    cur = mysql.connection.cursor()

    bestemming = get_one("bestemming", id, "id")
    form.luchthaven.data = bestemming["luchthaven"]
    form.land.data = bestemming["land"]
    form.stad.data = bestemming["stad"]

    if request.method == "POST" and form.validate_on_submit():
        land = request.form["land"]
        stad = request.form["stad"]
        luchthaven = request.form["luchthaven"]

        cur.execute("UPDATE bestemming SET luchthaven=%s, land=%s, stad=%s WHERE id=%s",
                    [stad, land, luchthaven, id])
        flash("luchthaven is gewijziged", "success")

        mysql.connection.commit()
        cur.close()
        return redirect(url_for("dashboard"))

    return render_template("flight/edit/edit_des.html", title="Bestemming", form=form, overview_title="Nieuwe Bestemming", icon_name="place", css_icon="place-icon")


@app.route("/edit-plane/<vliegtuig_id>", methods=['POST', 'GET'])
def edit_plane(vliegtuig_id):
    form = Plane(request.form)
    cur = mysql.connection.cursor()
    vliegtuig = get_one("vliegtuig", vliegtuig_id, "id")

    form.spanwijdte.data = vliegtuig["spanwijdte"]
    form.lengte.data = vliegtuig["lengte"]
    form.hoogte.data = vliegtuig["hoogte"]
    form.gewicht.data = vliegtuig["gewicht_bij_vertrek"]
    form.bereik.data = vliegtuig["bereik"]
    form.snelheid.data = vliegtuig["kruissnelheid"]
    form.locatie.data = vliegtuig["locatie"]
    form.aantal.data = vliegtuig["aantal_passagiers"]

    if request.method == "POST" and form.validate_on_submit():
        spanwijdte = request.form["spanwijdte"]
        lengte = request.form["lengte"]
        hoogte = request.form["hoogte"]
        gewicht = request.form["gewicht"]
        snelheid = request.form["snelheid"]
        aantal = request.form["aantal"]
        locatie = request.form["locatie"]
        bereik = request.form["bereik"]

        sql = "UPDATE vliegtuig SET spanwijdte=%s, lengte=%s, hoogte=%s, gewicht_bij_vertrek=%s, kruissnelheid=%s, bereik=%s, aantal_passagiers=%s, locatie=%s WHERE id=%s "

        cur.execute(sql, [spanwijdte, lengte, hoogte,
                    gewicht, snelheid, bereik, aantal,  locatie, vliegtuig_id])

        mysql.connection.commit()
        cur.close()

        flash("vliegtuig is gewijziged", "success")
        return redirect(url_for("dashboard"))

    return render_template("flight/edit/edit_plane.html", title="Vliegtuig", form=form, overview_title="Wijzig Vliegtuig", icon_name="flight", css_icon="plane-icon")
