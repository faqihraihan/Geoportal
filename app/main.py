from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route("/")
def beranda():
    return render_template("main.html")