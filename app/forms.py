from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Re-type Password", validators=[DataRequired(), EqualTo("password")])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    billing_address = StringField("Billing Address", validators=[DataRequired()])
    shipping_address = StringField("Shipping Address", validators=[DataRequired()])
    phone_number = StringField("Phone Number", validators=[DataRequired(), Length(min=10, max=15)])
    submit = SubmitField("Sign Up")

    def validate_user(self, username):
        user = User.query.filter_by(username=username.data).first()
        
        if user is not None:
            raise ValidationError("Please use a different username")
        
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        
        if email is not None:
            raise ValidationError("Please use a different e-mail address")
        
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")