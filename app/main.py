from msilib import add_data
from turtle import update
import folium
from folium.plugins import MousePosition
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Desa, Kecamatan, Kabupaten, Provinsi, User
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


#main data provinsi
@main.route("/input-data/data-provinsi")
@login_required
def input_data_provinsi():
    active = 'active'
    all_data = Provinsi.query.all()
    return render_template("input-data-provinsi.html", name=current_user.nama, input_data_navbar=active, provinsi=all_data)

@main.route("/input-data/data-provinsi/add", methods = ['POST'])
@login_required
def input_data_provinsi_add():
    if request.method == 'POST':
        id = request.form['id']
        nama = request.form['nama']
        
        provinsi = Provinsi.query.filter_by(id=id).first()
        if provinsi:
            flash('ID telah digunakan')
            return redirect(url_for('main.input_data_provinsi'))

        add_Data = Provinsi(id=id, nama=nama)

        db.session.add(add_Data)
        db.session.commit()
        flash("Data telah ditambahkan", "success")
        return redirect(url_for('main.input_data_provinsi'))

@main.route("/input-data/data-provinsi/update", methods = ['GET','POST'])
@login_required
def input_data_provinsi_update():
    if request.method == 'POST':
        update = Provinsi.query.get(request.form.get('id'))
        update.nama = request.form['nama']

        db.session.commit()
        flash("Data telah diubah", "success")
        return redirect(url_for('main.input_data_provinsi'))

@main.route("/input-data/data-provinsi/delete/<id>/", methods = ['GET','POST'])
@login_required
def input_data_provinsi_delete(id):
    delete = Provinsi.query.get(id)
    db.session.delete(delete)
    db.session.commit()
    flash("Data telah dihapus", "success")
    return redirect(url_for('main.input_data_provinsi'))

#main data kabupaten
@main.route("/input-data/data-kabupaten")
@login_required
def input_data_kabupaten():
    active = 'active'
    all_data = Kabupaten.query.all()
    return render_template("input-data-kabupaten.html", name=current_user.nama, input_data_navbar=active, kabupaten=all_data)

@main.route("/input-data/data-kabupaten/add", methods = ['POST'])
@login_required
def input_data_kabupaten_add():
    if request.method == 'POST':
        id = request.form['id']
        nama = request.form['nama']
        
        kabupaten = Kabupaten.query.filter_by(id=id).first()
        if kabupaten:
            flash('ID telah digunakan')
            return redirect(url_for('main.input_data_kabupaten'))

        add_Data = Kabupaten(id=id, nama=nama)

        db.session.add(add_Data)
        db.session.commit()
        flash("Data telah ditambahkan", "success")
        return redirect(url_for('main.input_data_kabupaten'))

@main.route("/input-data/data-kabupaten/update", methods = ['GET','POST'])
@login_required
def input_data_kabupaten_update():
    if request.method == 'POST':
        update = Kabupaten.query.get(request.form.get('id'))
        update.nama = request.form['nama']

        db.session.commit()
        flash("Data telah diubah", "success")
        return redirect(url_for('main.input_data_kabupaten'))

@main.route("/input-data/data-kabupaten/delete/<id>/", methods = ['GET','POST'])
@login_required
def input_data_kabupaten_delete(id):
    delete = Kabupaten.query.get(id)
    db.session.delete(delete)
    db.session.commit()
    flash("Data telah dihapus", "success")
    return redirect(url_for('main.input_data_kabupaten'))

#main data kecamatan
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

@main.route("/input-data/data-desa")
@login_required
def input_data_desa():
    active = 'active'
    all_data = Desa.query.all()
    return render_template("input-data-desa.html", name=current_user.nama, input_data_navbar=active, desa=all_data)

@main.route("/input-data/data-desa/add", methods = ['POST'])
@login_required
def input_data_desa_add():
    if request.method == 'POST':
        id_desa = request.form['id_desa']
        nama_desa = request.form['nama_desa']
        
        desa = Desa.query.filter_by(id_desa=id_desa).first()
        if desa:
            flash('ID telah digunakan')
            return redirect(url_for('main.input_data_desa'))

        add_Data = Desa(id_desa=id_desa, nama_desa=nama_desa)

        db.session.add(add_Data)
        db.session.commit()
        flash("Data telah ditambahkan")
        
        return redirect(url_for('main.input_data_desa'))

@main.route("/input-data/data-desa/update", methods = ['GET','POST'])
@login_required
def input_data_desa_update():
    if request.method == 'POST':
        update = Desa.query.get(request.form.get('id_desa'))
        update.nama_desa = request.form['nama_desa']

        db.session.commit()
        flash("Data telah diubah")

        return redirect(url_for('main.input_data_desa'))

@main.route("/input-data/data-desa/delete/<id_desa>/", methods = ['GET','POST'])
@login_required
def input_data_desa_delete(id_desa):
    delete = Desa.query.get(id_desa)
    db.session.delete(delete)
    db.session.commit()
    flash("Data telah dihapus")

    return redirect(url_for('main.input_data_desa'))

