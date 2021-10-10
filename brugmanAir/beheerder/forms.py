from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, length, EqualTo, Email


class RegisterForm(FlaskForm):
    fname = StringField("fname", [length(min=1, max=80), DataRequired()])
    lname = StringField("lname", [length(min=1, max=80), DataRequired()])
    straatnaam = StringField(
        "straatnaam", [length(min=1, max=80), DataRequired()])
    huisnr = IntegerField("huisnr", [DataRequired()])
    postcode = StringField("postcode", [length(min=6, max=6), DataRequired()])
    plaats = StringField("plaats", [length(min=1, max=80), DataRequired()])
    email = StringField(
        "Email", [length(min=6, max=120), DataRequired(), Email()])
    password = PasswordField("password", [length(min=4, max=80),
                                          DataRequired(),
                                          EqualTo(
        "confirm", message="Passwords do not match")
    ])
    confirm = PasswordField("confirm", [DataRequired()])
