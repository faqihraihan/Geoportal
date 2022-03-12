import folium
from folium.plugins import MousePosition
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route("/")
def home():
    if current_user.is_authenticated:
        return render_template("main.html", name=current_user.nama)
    return render_template("main.html")

@main.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.nama)

@main.route("/input_data")
@login_required
def input_data():
    return render_template("input-data.html", name=current_user.nama)

@main.route("/gis", methods=['GET', 'POST'])
def gis():
    map = folium.Map(
            location=[-1.1265694, 118.6380067], zoom_start=5, tiles="cartodbpositron", min_zoom=5, zoom_control=True
    )

    formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
    MousePosition(
        position="bottomleft",
        separator=" | ",
        empty_string="NaN",
        lng_first=True,
        num_digits=20,
        prefix="Kordinat:",
        lat_formatter=formatter,
        lng_formatter=formatter,
    ).add_to(map)

    map.save("app/templates/gis-maps.html")
    return render_template("maps.html")