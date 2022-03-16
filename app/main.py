from msilib import add_data
from turtle import update
import folium
from folium.plugins import MousePosition
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Kecamatan, User
from . import db

main = Blueprint('main', __name__)

@main.route("/")
def home():
    if current_user.is_authenticated:
        return render_template("main.html", name=current_user.nama)
    return render_template("main.html")

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

@main.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.nama)

@main.route("/input-data")
@login_required
def input_data():
    active = 'active'
    return render_template("input-data.html", name=current_user.nama, input_data_navbar=active)

@main.route("/input-data/data-kecamatan")
@login_required
def input_data_kecamatan():
    active = 'active'
    all_data = Kecamatan.query.all()
    return render_template("input-data-kecamatan.html", name=current_user.nama, input_data_navbar=active, kecamatan=all_data)

@main.route("/input-data/data-kecamatan/add", methods = ['POST'])
@login_required
def input_data_kecamatan_add():
    if request.method == 'POST':
        id = request.form['id']
        nama = request.form['nama']
        
        kecamatan = Kecamatan.query.filter_by(id=id).first()
        if kecamatan:
            flash('ID telah digunakan')
            return redirect(url_for('main.input_data_kecamatan'))

        add_Data = Kecamatan(id=id, nama=nama)

        db.session.add(add_Data)
        db.session.commit()
        flash("Data telah ditambahkan")
        
        return redirect(url_for('main.input_data_kecamatan'))

@main.route("/input-data/data-kecamatan/update", methods = ['GET','POST'])
@login_required
def input_data_kecamatan_update():
    if request.method == 'POST':
        update = Kecamatan.query.get(request.form.get('id'))
        update.nama = request.form['nama']

        db.session.commit()
        flash("Data telah diubah")

        return redirect(url_for('main.input_data_kecamatan'))

@main.route("/input-data/data-kecamatan/delete/<id>/", methods = ['GET','POST'])
@login_required
def input_data_kecamatan_delete(id):
    delete = Kecamatan.query.get(id)
    db.session.delete(delete)
    db.session.commit()
    flash("Data telah dihapus")

    return redirect(url_for('main.input_data_kecamatan'))