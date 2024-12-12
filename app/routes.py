from flask import render_template, redirect, flash, url_for
from flask_login import current_user, login_required, login_user, logout_user
from app import app, db
from app.forms import RegistrationForm, LoginForm
from app.models import User

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
    
    return render_template("register.html", title="Sign Up", form=form)

@app.route("/log-in", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.verify_password(form.password.data):
            flash("Invalid username and/or password", "error")  # Category added
            
            return redirect(url_for("login"))
        
        login_user(user)
        flash("Login successful!", "success")  # Category added

        return redirect(url_for("home"))
    
    return render_template("login.html", title="Log In", form=form)

@app.route("/log-out")
def logout():
    logout_user()

    flash("You have successfully logged out", "success")  # Category added

    return redirect(url_for("home"))
