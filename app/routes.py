from flask import render_template, redirect, flash, url_for, make_response
from flask_login import current_user, login_required, login_user, logout_user
from app import app, db
from app.forms import RegistrationForm, LoginForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User
from datetime import datetime, timedelta
import random, string

@app.route("/")
def home():
    return render_template("home.html", title="Home")

@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    
    form = RegistrationForm()

    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data, 
            billing_address=form.billing_address.data, 
            shipping_address=form.shipping_address.data,
            phone_number=form.phone_number.data
        )

        new_user.set_password(form.password.data)

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please log in", "success")  # Correct category
        return redirect(url_for("login"))
    
    response = make_response(render_template("register.html", title="Sign Up", form=form))
    response.headers["Cache-Control"] = "no-store"
    return response

@app.route("/log-in", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.verify_password(form.password.data):
            flash("Invalid username and/or password", "error")
            
            return redirect(url_for("login"))
        
        login_user(user)

        return redirect(url_for("home"))
    
    response = make_response(render_template("login.html", title="Log In", form=form))
    response.headers["Cache-Control"] = "no-store"
    return response

def generate_reset_token(length=64):
    """Generates a random reset token of specified length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

from flask import render_template, request, flash, redirect, url_for
from flask_mail import Message
from datetime import datetime, timedelta
from app import mail
from app.models import User
from app.forms import ResetPasswordRequestForm

@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    form = ResetPasswordRequestForm()

    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()

        if user:
            # Step 1: Generate the password reset token
            token = generate_reset_token()

            # Step 2: Set the token and expiration in the user's record
            user.password_reset_token = token
            user.reset_token_expiration = datetime.utcnow() + timedelta(hours=1)

            db.session.commit()

            # Step 3: Generate the reset link with the token
            reset_link = url_for("reset_password_with_token", token=token, _external=True)

            print(f"Password reset link: {reset_link}")

            flash(f"Password reset link generated. Check the console for the link", "info")

            return redirect(url_for("login"))  # Redirect to the login page after sending the email
        else:
            flash("No account found with that email address", "error")

    response = make_response(render_template("reset_password.html", form=form))
    response.headers["Cache-Control"] = "no-store"
    return response

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password_with_token(token):
    # Find the user with the reset token
    user = User.query.filter_by(password_reset_token=token).first()
    
    # Check if the token exists and is not expired
    if not user or user.reset_token_expiration < datetime.utcnow():
        flash("Invalid or expired token. Please try again.", "error")
        return redirect(url_for('reset_password'))

    # Create the password reset form
    form = ResetPasswordForm()

    if form.validate_on_submit():
        # Set the new password using the set_password method
        new_password = form.password.data
        user.set_password(new_password)  # This will hash the password

        # Clear the reset token and expiration date after use
        user.password_reset_token = None
        user.reset_token_expiration = None
        db.session.commit()

        flash('Your password has been successfully reset.', 'success')
        return redirect(url_for('login'))  # Redirect to login page after successful reset

    response = make_response(render_template('reset_password_with_token.html', form=form, token=token))
    response.headers["Cache-Control"] = "no-data"
    return response

@app.route("/log-out")
def logout():
    logout_user()

    flash("You have successfully logged out", "success")  # Category added

    return redirect(url_for("home"))
