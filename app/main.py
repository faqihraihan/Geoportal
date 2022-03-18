import folium
import base64
from folium.plugins import MousePosition
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user
from .models import Kelompok_Tani, User, Desa, Kecamatan, Kabupaten, Provinsi
from . import db

main = Blueprint('main', __name__)

@main.route("/")
def home():
    if current_user.is_authenticated:
        image=None
        if current_user.img:
            image = base64.b64encode(current_user.img).decode('ascii')

        return render_template("main.html", img = image, name=current_user.nama)
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

    poktan = Kelompok_Tani.query.count()

    image=None
    if current_user.img:
        image = base64.b64encode(current_user.img).decode('ascii')
    return render_template('dashboard.html', img = image, name=current_user.nama, level=current_user.lvl, poktan=poktan)

@main.route("/input-data")
@login_required
def input_data():
    image=None
    if current_user.img:
        image = base64.b64encode(current_user.img).decode('ascii')
    active = 'active'
    return render_template("input-data.html", img = image, name=current_user.nama, level=current_user.lvl, input_data_navbar=active)

@main.route("/profil")
@login_required
def profil():
    return redirect(url_for('main.profil_me'))

@main.route("/profil/me", methods = ['GET', 'POST'])
@login_required
def profil_me():
    all_data = User.query.all()

    image=None
    if current_user.img:
        image = base64.b64encode(current_user.img).decode('ascii')
    active = 'active'

    return render_template("profil.html", img = image, id=current_user.id, name=current_user.nama, email=current_user.email, nohp=current_user.nohp, level=current_user.lvl, profil_navbar=active, user=all_data)

@main.route("/input-data/data-desa")
@login_required
def input_data_desa():
    active = 'active'

    image=None
    if current_user.img:
        image = base64.b64encode(current_user.img).decode('ascii')

    all_data = Desa.query.all()
    return render_template("input-data-desa.html", img = image, name=current_user.nama, level=current_user.lvl, input_data_desa_navbar=active, input_data_master_navbar=active, desa=all_data)

@main.route("/input-data/data-desa/add", methods = ['POST'])
@login_required
def input_data_desa_add():
    if request.method == 'POST':
        id = request.form['id']
        nama = request.form['nama']

        desa = Desa.query.filter_by(id=id).first()
        if desa: 
            flash('ID telah digunakan')
            return redirect(url_for('main.input_data_desa'))

        add_Data = Desa(id=id, nama=nama)
        
        db.session.add(add_Data)
        db.session.commit()
        flash("Data berhasil ditambahkan")
 
        return redirect(url_for('main.input_data_desa'))

@main.route("/input-data/data-desa/update", methods = ['GET', 'POST'])
@login_required
def input_data_desa_update():
    if request.method == 'POST':
        update = Desa.query.get(request.form.get('id_desa'))
        update.id = request.form['id']
        update.nama = request.form['nama']
 
        db.session.commit()
        flash("Data berhasil diubah")
 
        return redirect(url_for('main.input_data_desa'))

@main.route("/input-data/data-desa/delete/<id>/", methods = ['GET', 'POST'])
@login_required
def input_data_desa_delete(id):
    delete = Desa.query.get(id)
    db.session.delete(delete)
    db.session.commit()
    flash("Data berhasil dihapus")
 
    return redirect(url_for('main.input_data_desa'))

@main.route("/input-data/data-kecamatan")
@login_required
def input_data_kecamatan():
    active = 'active'

    image=None
    if current_user.img:
        image = base64.b64encode(current_user.img).decode('ascii')

    all_data = Kecamatan.query.all()
    return render_template("input-data-kecamatan.html", img = image, name=current_user.nama, level=current_user.lvl, input_data_kecamatan_navbar=active, input_data_master_navbar=active, kecamatan=all_data)

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
        flash("Data berhasil ditambahkan")
 
        return redirect(url_for('main.input_data_kecamatan'))

@main.route("/input-data/data-kecamatan/update", methods = ['GET', 'POST'])
@login_required
def input_data_kecamatan_update():
    if request.method == 'POST':
        update = Kecamatan.query.get(request.form.get('id_kecamatan'))
        update.id = request.form['id']
        update.nama = request.form['nama']
 
        db.session.commit()
        flash("Data berhasil diubah")
 
        return redirect(url_for('main.input_data_kecamatan'))

@main.route("/input-data/data-kecamatan/delete/<id>/", methods = ['GET', 'POST'])
@login_required
def input_data_kecamatan_delete(id):
    delete = Kecamatan.query.get(id)
    db.session.delete(delete)
    db.session.commit()
    flash("Data berhasil dihapus")
 
    return redirect(url_for('main.input_data_kecamatan'))

@main.route("/input-data/data-kabupaten")
@login_required
def input_data_kabupaten():
    active = 'active'

    image=None
    if current_user.img:
        image = base64.b64encode(current_user.img).decode('ascii')

    all_data = Kabupaten.query.all()
    return render_template("input-data-kabupaten.html", img = image, name=current_user.nama, level=current_user.lvl, input_data_kabupaten_navbar=active, input_data_master_navbar=active, kabupaten=all_data)

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
        flash("Data berhasil ditambahkan")
 
        return redirect(url_for('main.input_data_kabupaten'))

@main.route("/input-data/data-kabupaten/update", methods = ['GET', 'POST'])
@login_required
def input_data_kabupaten_update():
    if request.method == 'POST':
        update = Kabupaten.query.get(request.form.get('id_kabupaten'))
        update.id = request.form['id']
        update.nama = request.form['nama']
 
        db.session.commit()
        flash("Data berhasil diubah")
 
        return redirect(url_for('main.input_data_kabupaten'))

@main.route("/input-data/data-kabupaten/delete/<id>/", methods = ['GET', 'POST'])
@login_required
def input_data_kabupaten_delete(id):
    delete = Kabupaten.query.get(id)
    db.session.delete(delete)
    db.session.commit()
    flash("Data berhasil dihapus")
 
    return redirect(url_for('main.input_data_kabupaten'))

@main.route("/input-data/data-provinsi")
@login_required
def input_data_provinsi():
    active = 'active'

    image=None
    if current_user.img:
        image = base64.b64encode(current_user.img).decode('ascii')

    all_data = Provinsi.query.all()
    return render_template("input-data-provinsi.html", img = image, name=current_user.nama, level=current_user.lvl, input_data_provinsi_navbar=active, input_data_master_navbar=active, provinsi=all_data)

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
        flash("Data berhasil ditambahkan")
 
        return redirect(url_for('main.input_data_provinsi'))

@main.route("/input-data/data-provinsi/update", methods = ['GET', 'POST'])
@login_required
def input_data_provinsi_update():
    if request.method == 'POST':
        update = Provinsi.query.get(request.form.get('id_provinsi'))
        update.id = request.form['id']
        update.nama = request.form['nama']
 
        db.session.commit()
        flash("Data berhasil diubah")
 
        return redirect(url_for('main.input_data_provinsi'))

@main.route("/input-data/data-provinsi/delete/<id>/", methods = ['GET', 'POST'])
@login_required
def input_data_provinsi_delete(id):
    delete = Provinsi.query.get(id)
    db.session.delete(delete)
    db.session.commit()
    flash("Data berhasil dihapus")
 
    return redirect(url_for('main.input_data_provinsi'))

@main.route("/input-data/data-kelompok-tani")
@login_required
def input_data_kelompok_tani():
    active = 'active'

    image=None
    if current_user.img:
        image = base64.b64encode(current_user.img).decode('ascii')

    all_data = Kelompok_Tani.query.all()
    return render_template("input-data-kelompok-tani.html", img = image, name=current_user.nama, level=current_user.lvl, input_data_kelompok_tani_navbar=active, input_data_pertanian_navbar=active, kelompok_tani=all_data)

@main.route("/input-data/data-kelompok-tani/add", methods = ['POST'])
@login_required
def input_data_kelompok_tani_add():
    if request.method == 'POST':
        id = request.form['id']
        nama = request.form['nama']
        no_sk = request.form['no_sk']

        kelompok_tani = Kelompok_Tani.query.filter_by(id=id).first()
        if kelompok_tani: 
            flash('ID telah digunakan')
            return redirect(url_for('main.input_data_kelompok_tani'))

        add_Data = Kelompok_Tani(id=id, nama=nama, no_sk=no_sk)
        
        db.session.add(add_Data)
        db.session.commit()
        flash("Data berhasil ditambahkan")
 
        return redirect(url_for('main.input_data_kelompok_tani'))

@main.route("/input-data/data-kelompok-tani/update", methods = ['GET', 'POST'])
@login_required
def input_data_kelompok_tani_update():
    if request.method == 'POST':
        update = Kelompok_Tani.query.get(request.form.get('id_kelompok_tani'))
        update.id = request.form['id']
        update.nama = request.form['nama']
        update.no_sk = request.form['no_sk']
 
        db.session.commit()
        flash("Data berhasil diubah")
 
        return redirect(url_for('main.input_data_kelompok_tani'))

@main.route("/input-data/data-kelompok-tani/delete/<id>/", methods = ['GET', 'POST'])
@login_required
def input_data_kelompok_tani_delete(id):
    delete = Kelompok_Tani.query.get(id)
    db.session.delete(delete)
    db.session.commit()
    flash("Data berhasil dihapus")
 
    return redirect(url_for('main.input_data_kelompok_tani'))