from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField
from wtforms.validators import DataRequired, length, Email


class Medewerker(FlaskForm):
    fname = StringField("fname", [length(min=1, max=80), DataRequired()])
    lname = StringField("lname", [length(min=1, max=80), DataRequired()])
    postcode = StringField("postcode", [length(min=6, max=6), DataRequired()])
    email = StringField(
        "Email", [length(min=6, max=120), DataRequired(), Email()])


class Bestemming(FlaskForm):
    land = StringField("land", [length(min=1, max=80), DataRequired()])
    stad = StringField("stad", [length(min=1, max=80), DataRequired()])
    luchthaven = StringField(
        "luchthaven", [length(min=1, max=80), DataRequired()])


class Plane(FlaskForm):
    spanwijdte = FloatField(
        "spanwijdte", [DataRequired()])
    lengte = FloatField(
        "lengte", [DataRequired()])
    hoogte = FloatField(
        "hoogte", [DataRequired()])
    gewicht = FloatField(
        "spanwijdte", [DataRequired()])
    snelheid = IntegerField(
        "snelheid", [DataRequired()])
    bereik = IntegerField(
        "bereik", [DataRequired()])
    aantal = IntegerField(
        "aantal", [DataRequired()])
    locatie = StringField("locatie", [length(min=1, max=120), DataRequired()])
