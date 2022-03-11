from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template("main.html")

@main.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.nama)

@main.route("/input_data")
@login_required
def input_data():
    return render_template("input-data.html", name=current_user.nama)