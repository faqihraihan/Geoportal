import os
import numpy as np
import patoolib
import folium
import base64
import geopandas as gpd
from folium.plugins import MousePosition
from flask import Blueprint, render_template, url_for, redirect, request, flash, jsonify
from flask_login import login_required, current_user
from bs4 import BeautifulSoup
import requests
from .models import Provinsi, Kabupaten, Kecamatan, Desa, Gapoktan, Kelompok_Tani, Petani, Lahan, Komoditas, Pupuk, Hama, Racun, User, Log_Tanam, Detail_Log_Tanam_Pupuk, Detail_Log_Tanam_Hama, Detail_Log_Tanam_Racun
from . import db

main = Blueprint('main', __name__)


@ main.route("/")
def home():
    url = 'https://hargapangan.id/tabel-harga/pedagang-besar/daerah'
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    val_time = soup.findAll("tr")[0]
    arr_time = []
    for i in range(2, 8):
        time = val_time.findAll("th")[i].text.replace('"', '')
        arr_time.append(time)

    val_price = soup.findAll("tr")[1]
    arr_price = []
    for j in range(2, 8):
        price = val_price.findAll("td")[j].text.replace(
            '.', '').replace('"', '')
        arr_price.append(price)

    data = {'time': arr_time, 'price': arr_price}

    if current_user.is_authenticated:
        image = None
        if current_user.foto:
            image = base64.b64encode(current_user.foto).decode('ascii')

        return render_template("main.html", foto=image, name=current_user.nama, data=data)
    return render_template("main.html", data=data)


@ main.route("/gis", methods=['GET', 'POST'])
@ main.route("/gis/<id>", methods=['GET', 'POST'])
def gis(id=None):
    if id:
        data = Desa.query.filter_by(id_desa=id).first()

        layer = gpd.read_file(data.polygon)
        layer = layer.to_crs("EPSG:4326")

        m = folium.Map(location=[-1.1265694, 118.6380067],
            zoom_start=5, min_zoom=5)

        for x in layer.index:
            color = np.random.randint(16, 256, size=3)
            color = [str(hex(i))[2:] for i in color]
            color = '#'+''.join(color).upper()
            layer.at[x, 'color'] = color

        def style(feature):
            return {
                'fillColor': feature['properties']['color'],
                'color': feature['properties']['color'],
                'weight': 1,
                'fillOpacity': 0.7
            }

        gjson = folium.GeoJson(layer, name=data.nama, style_function=style).add_to(m)

        m.fit_bounds(gjson.get_bounds())

        folium.Popup(data.nama).add_to(gjson)

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
        ).add_to(m)

        tile_layer = folium.TileLayer(
            tiles="http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}",
            attr='google.com',
            max_zoom=19,
            name='darkmatter',
            control=False,
            opacity=1
        )
        tile_layer.add_to(m)

        m.save("app/templates/gis-maps.html")
        return render_template("maps.html", data=data, id=id)

    m = folium.Map(location=[-1.1265694, 118.6380067],
                   zoom_start=5, min_zoom=5)

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
    ).add_to(m)

    tile_layer = folium.TileLayer(
        tiles="http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}",
        attr='google.com',
        max_zoom=19,
        name='darkmatter',
        control=False,
        opacity=1
    )
    tile_layer.add_to(m)

    m.save("app/templates/gis-maps.html")
    return render_template("maps.html")


@ main.route("/profil")
@ login_required
def profil():
    return redirect(url_for('main.profil_me'))


@ main.route("/profil/me", methods=['GET', 'POST'])
@ login_required
def profil_me():
    all_data = User.query.all()

    image = None
    if current_user.foto:
        image = base64.b64encode(current_user.foto).decode('ascii')
    active = 'active'

    return render_template("profil.html", foto=image, id=current_user.id_users, name=current_user.nama, email=current_user.email, telp=current_user.telp, level=current_user.level, profil_navbar=active, user=all_data)


@ main.route("/dashboard")
@ login_required
def dashboard():
    poktan = Kelompok_Tani.query.count()
    gapoktan = Gapoktan.query.count()

    image = None
    if current_user.foto:
        image = base64.b64encode(current_user.foto).decode('ascii')
    active = 'active'
    return render_template('dashboard.html', foto=image, name=current_user.nama, level=current_user.level, poktan=poktan, gapoktan=gapoktan, dashboard_navbar=active)


@ main.route("/dashboard/gapoktan")
@ login_required
def dashboard_gapoktan():
    image = None
    if current_user.foto:
        image = base64.b64encode(current_user.foto).decode('ascii')

    all_data = Gapoktan.query.all()
    return render_template("dashboard-gapoktan.html", foto=image, name=current_user.nama, level=current_user.level, gapoktan=all_data)


@ main.route("/dashboard/kelompok_tani")
@ login_required
def dashboard_kelompok_tani():
    image = None
    if current_user.foto:
        image = base64.b64encode(current_user.foto).decode('ascii')

    all_data = Kelompok_Tani.query.all()
    return render_template("dashboard-kelompok-tani.html", foto=image, name=current_user.nama, level=current_user.level, kelompok_tani=all_data)


@ main.route("/input-data")
@ login_required
def input_data():
    poktan = Kelompok_Tani.query.count()
    gapoktan = Gapoktan.query.count()

    image = None
    if current_user.foto:
        image = base64.b64encode(current_user.foto).decode('ascii')
    active = 'active'
    return render_template("input-data.html", foto=image, name=current_user.nama, level=current_user.level, poktan=poktan, gapoktan=gapoktan, input_data_navbar=active)


@ main.route("/input-data/data-provinsi")
@ login_required
def input_data_provinsi():
    active = 'active'

    image = None
    if current_user.foto:
        image = base64.b64encode(current_user.foto).decode('ascii')

    all_data = Provinsi.query.all()
    return render_template("input-data-provinsi.html", foto=image, name=current_user.nama, level=current_user.level, input_data_provinsi_navbar=active, input_data_master_navbar=active, provinsi=all_data)


@ main.route("/input-data/data-provinsi/add", methods=['POST'])
@ login_required
def input_data_provinsi_add():
    if request.method == 'POST':
        id_prov = request.form['id_prov']
        nama = request.form['nama']

        prov = Provinsi.query.filter_by(id_prov=id_prov).first()
        if prov:
            flash('ID telah digunakan')
            return redirect(url_for('main.input_data_provinsi'))

        add_Data = Provinsi(id_prov=id_prov, nama=nama)

        db.session.add(add_Data)
        db.session.commit()
        flash("Data berhasil ditambahkan")

        return redirect(url_for('main.input_data_provinsi'))


@ main.route("/input-data/data-provinsi/update", methods=['GET', 'POST'])
@ login_required
def input_data_provinsi_update():
    if request.method == 'POST':
        update = Provinsi.query.get(request.form.get('id_provinsi'))
        update.nama = request.form['nama']

        db.session.commit()
        flash("Data berhasil diubah")

        return redirect(url_for('main.input_data_provinsi'))


@ main.route("/input-data/data-provinsi/delete", methods=['GET', 'POST'])
@ login_required
def input_data_provinsi_delete():
    id_prov = request.form['id']
    delete = Provinsi.query.get(id_prov)

    db.session.delete(delete)
    db.session.commit()
    flash("Data berhasil dihapus")

    return redirect(url_for('main.input_data_provinsi'))


@ main.route("/input-data/data-kabupaten")
@ login_required
def input_data_kabupaten():
    active = 'active'

    image = None
    if current_user.foto:
        image = base64.b64encode(current_user.foto).decode('ascii')

    provinsi = Provinsi.query.all()
    all_data = Kabupaten.query.all()
    return render_template("input-data-kabupaten.html", foto=image, name=current_user.nama, level=current_user.level, input_data_kabupaten_navbar=active, input_data_master_navbar=active, provinsi=provinsi, kabupaten=all_data)


@ main.route("/input-data/data-kabupaten/live-search", methods=['GET', 'POST'])
@ login_required
def live_search_data_kabupaten():
    if request.method == 'POST':
        id = request.form['provinsi_response']
        kabupaten = Kabupaten.query.filter(Kabupaten.id_prov.like(id))
    return jsonify({'htmlresponse': render_template('data-kabupaten-response.html', kabupaten=kabupaten)})


@ main.route("/input-data/data-kabupaten/add", methods=['POST'])
@ login_required
def input_data_kabupaten_add():
    if request.method == 'POST':
        id_prov = request.form['provinsi']
        id_kab = request.form['id_kab']
        id = id_prov+id_kab
        nama = request.form['nama']

        kab = Kabupaten.query.filter_by(id_kab=id).first()
        if kab:
            flash('ID telah digunakan')
            return redirect(url_for('main.input_data_kabupaten'))

        add_Data = Kabupaten(id_kab=id, id_prov=id_prov, nama=nama)

        db.session.add(add_Data)
        db.session.commit()
        flash("Data berhasil ditambahkan")

        return redirect(url_for('main.input_data_kabupaten'))


@ main.route("/input-data/data-kabupaten/update", methods=['GET', 'POST'])
@ login_required
def input_data_kabupaten_update():
    if request.method == 'POST':
        update = Kabupaten.query.get(request.form.get('id_kabupaten'))
        update.nama = request.form['nama']

        db.session.commit()
        flash("Data berhasil diubah")

        return redirect(url_for('main.input_data_kabupaten'))


@ main.route("/input-data/data-kabupaten/delete", methods=['GET', 'POST'])
@ login_required
def input_data_kabupaten_delete():
    id_kab = request.form['id_kab']
    delete = Kabupaten.query.get(id_kab)

    db.session.delete(delete)
    db.session.commit()
    flash("Data berhasil dihapus")

    return redirect(url_for('main.input_data_kabupaten'))


@ main.route("/input-data/data-kecamatan")
@ login_required
def input_data_kecamatan():
    active = 'active'

    image = None
    if current_user.foto:
        image = base64.b64encode(current_user.foto).decode('ascii')

    provinsi = Provinsi.query.all()
    all_data = Kecamatan.query.all()
    return render_template("input-data-kecamatan.html", foto=image, name=current_user.nama, level=current_user.level, input_data_kecamatan_navbar=active, input_data_master_navbar=active, provinsi=provinsi, kecamatan=all_data)


@ main.route("/input-data/data-kecamatan/live-search", methods=['GET', 'POST'])
@ login_required
def live_search_data_kecamatan():
    if request.method == 'POST':
        id = request.form['kabupaten_response']
        kecamatan = Kecamatan.query.filter(Kecamatan.id_kab.like(id))
    return jsonify({'htmlresponse': render_template('data-kecamatan-response.html', kecamatan=kecamatan)})


@ main.route("/input-data/data-kecamatan/add", methods=['POST'])
@ login_required
def input_data_kecamatan_add():
    if request.method == 'POST':
        id_kab = request.form['kabupaten']
        id_kec = request.form['id_kec']
        id = id_kab+id_kec
        nama = request.form['nama']

        kec = Kecamatan.query.filter_by(id_kec=id).first()
        if kec:
            flash('ID telah digunakan')
            return redirect(url_for('main.input_data_kecamatan'))

        add_Data = Kecamatan(id_kec=id, id_kab=id_kab, nama=nama)

        db.session.add(add_Data)
        db.session.commit()
        flash("Data berhasil ditambahkan")

        return redirect(url_for('main.input_data_kecamatan'))


@ main.route("/input-data/data-kecamatan/update", methods=['GET', 'POST'])
@ login_required
def input_data_kecamatan_update():
    if request.method == 'POST':
        update = Kecamatan.query.get(request.form.get('id_kecamatan'))
        update.nama = request.form['nama']

        db.session.commit()
        flash("Data berhasil diubah")

        return redirect(url_for('main.input_data_kecamatan'))


@ main.route("/input-data/data-kecamatan/delete", methods=['GET', 'POST'])
@ login_required
def input_data_kecamatan_delete():
    id_kec = request.form['id_kec']
    delete = Kecamatan.query.get(id_kec)

    db.session.delete(delete)
    db.session.commit()
    flash("Data berhasil dihapus")

    return redirect(url_for('main.input_data_kecamatan'))


@ main.route("/input-data/data-desa")
@ login_required
def input_data_desa():
    active = 'active'

    image = None
    if current_user.foto:
        image = base64.b64encode(current_user.foto).decode('ascii')

    provinsi = Provinsi.query.all()
    all_data = Desa.query.all()
    return render_template("input-data-desa.html", foto=image, name=current_user.nama, level=current_user.level, input_data_desa_navbar=active, input_data_master_navbar=active, provinsi=provinsi, desa=all_data)


@ main.route("/input-data/data-desa/live-search", methods=['GET', 'POST'])
@ login_required
def live_search_data_desa():
    if request.method == 'POST':
        id = request.form['kecamatan_response']
        desa = Desa.query.filter(Desa.id_kec.like(id))
    return jsonify({'htmlresponse': render_template('data-desa-response.html', desa=desa)})


@ main.route("/input-data/data-desa/add", methods=['POST'])
@ login_required
def input_data_desa_add():
    if request.method == 'POST':
        id_kec = request.form['kecamatan']
        id_desa = request.form['id_desa']
        id = id_kec+id_desa
        nama = request.form['nama']
        file = request.files['json']

        desa = Desa.query.filter_by(id_desa=id).first()
        if desa:
            flash('ID telah digunakan')
            return redirect(url_for('main.input_data_desa'))

        json = "{}.json".format(id)
        extfile = file.filename.rsplit('.', 1)[1].lower()

        file.save(os.path.join("app/static/json/temporary", "{}.{}".format(id, extfile)))
        patoolib.extract_archive("app/static/json/temporary/{}.{}".format(id, extfile), outdir="app/static/json/temporary/")

        dir = 'app/static/json/temporary'
        search_shp = [f for f in os.listdir(dir) if f.endswith(".shp")]

        gjson = gpd.read_file("app/static/json/temporary/{}".format(search_shp[0]))
        gjson.to_file("app/static/json/temporary/{}".format(json), driver='GeoJSON')
        gjson = gjson.to_json()

        add_Data = Desa(id_desa=id, id_kec=id_kec, nama=nama, polygon=gjson)

        db.session.add(add_Data)
        db.session.commit()

        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))

        flash("Data berhasil ditambahkan")

        return redirect(url_for('main.input_data_desa'))


@ main.route("/input-data/data-desa/update", methods=['GET', 'POST'])
@ login_required
def input_data_desa_update():
    if request.method == 'POST':
        update = Desa.query.get(request.form.get('id_desa'))
        update.nama = request.form['nama']
        id = request.form['id_desa']
        file = request.files['json']

        if file:
            json = "{}.json".format(id)
            extfile = file.filename.rsplit('.', 1)[1].lower()

            file.save(os.path.join("app/static/json/temporary", "{}.{}".format(id, extfile)))
            patoolib.extract_archive("app/static/json/temporary/{}.{}".format(id, extfile), outdir="app/static/json/temporary/")

            dir = 'app/static/json/temporary'
            search_shp = [f for f in os.listdir(dir) if f.endswith(".shp")]

            gjson = gpd.read_file("app/static/json/temporary/{}".format(search_shp[0]))
            gjson.to_file("app/static/json/temporary/{}".format(json), driver='GeoJSON')
            gjson = gjson.to_json()

            update.polygon = gjson

            for f in os.listdir(dir):
                os.remove(os.path.join(dir, f))

        db.session.commit()
        flash("Data berhasil diubah")

        return redirect(url_for('main.input_data_desa'))


@ main.route("/input-data/data-desa/delete", methods=['GET', 'POST'])
@ login_required
def input_data_desa_delete():
    id_desa = request.form['id_desa']
    delete = Desa.query.get(id_desa)

    db.session.delete(delete)
    db.session.commit()
    flash("Data berhasil dihapus")

    return redirect(url_for('main.input_data_desa'))


@ main.route("/input-data/data-gapoktan")
@ login_required
def input_data_gapoktan():
    active = 'active'

    image = None
    if current_user.foto:
        image = base64.b64encode(current_user.foto).decode('ascii')

    provinsi = Provinsi.query.all()
    all_data = Gapoktan.query.all()
    return render_template("input-data-gapoktan.html", foto=image, name=current_user.nama, level=current_user.level, input_data_gapoktan_navbar=active, input_data_pertanian_navbar=active, gapoktan=all_data, provinsi=provinsi)


@ main.route("/input-data/data-gapoktan/add", methods=['POST'])
@ login_required
def input_data_gapoktan_add():
    if request.method == 'POST':
        id_desa = request.form['desa']
        id_gapoktan = request.form['id_gapoktan']
        id = id_desa+id_gapoktan
        nama = request.form['nama']
        ketua = request.form['ketua']
        telp = request.form['telp']
        no_sk = request.form['no-sk']

        gapoktan = Gapoktan.query.filter_by(id_gapoktan=id).first()
        if gapoktan:
            flash('ID telah digunakan')
            return redirect(url_for('main.input_data_gapoktan'))

        add_Data = Gapoktan(id_gapoktan=id, id_desa=id_desa, nama=nama, ketua=ketua, telp=telp, no_sk=no_sk)

        db.session.add(add_Data)
        db.session.commit()
        flash("Data berhasil ditambahkan")

        return redirect(url_for('main.input_data_gapoktan'))


@ main.route("/input-data/data-gapoktan/update", methods=['GET', 'POST'])
@ login_required
def input_data_gapoktan_update():
    if request.method == 'POST':
        update = Gapoktan.query.get(request.form.get('id_gapoktan'))
        update.nama = request.form['nama']
        update.ketua = request.form['ketua']
        update.telp = request.form['telp']
        update.no_sk = request.form['no-sk']

        db.session.commit()
        flash("Data berhasil diubah")

        return redirect(url_for('main.input_data_gapoktan'))


@ main.route("/input-data/data-gapoktan/delete", methods=['GET', 'POST'])
@ login_required
def input_data_gapoktan_delete():
    id_gapoktan = request.form['id_gapoktan']
    delete = Gapoktan.query.get(id_gapoktan)

    db.session.delete(delete)
    db.session.commit()
    flash("Data berhasil dihapus")

    return redirect(url_for('main.input_data_gapoktan'))


@ main.route("/input-data/data-kelompok-tani")
@ login_required
def input_data_kelompok_tani():
    active = 'active'

    image = None
    if current_user.foto:
        image = base64.b64encode(current_user.foto).decode('ascii')

    provinsi = Provinsi.query.all()
    all_data = Kelompok_Tani.query.all()
    return render_template("input-data-kelompok-tani.html", foto=image, name=current_user.nama, level=current_user.level, input_data_kelompok_tani_navbar=active, input_data_pertanian_navbar=active, kelompok_tani=all_data, provinsi=provinsi)


@ main.route("/input-data/data-kelompok-tani/add", methods=['POST'])
@ login_required
def input_data_kelompok_tani_add():
    if request.method == 'POST':
        id_desa = request.form['desa']
        id_poktan = request.form['id_poktan']
        id = id_desa+id_poktan
        nama = request.form['nama']
        telp = request.form['telp']
        no_sk = request.form['no-sk']

        poktan = Kelompok_Tani.query.filter_by(id_poktan=id).first()
        if poktan:
            flash('ID telah digunakan')
            return redirect(url_for('main.input_data_kelompok_tani'))

        add_Data = Kelompok_Tani(id_poktan=id, id_desa=id_desa, nama=nama, telp=telp, no_sk=no_sk)

        db.session.add(add_Data)
        db.session.commit()
        flash("Data berhasil ditambahkan")

        return redirect(url_for('main.input_data_kelompok_tani'))


@ main.route("/input-data/data-kelompok-tani/update", methods=['GET', 'POST'])
@ login_required
def input_data_kelompok_tani_update():
    if request.method == 'POST':
        update = Kelompok_Tani.query.get(request.form.get('id_kelompok_tani'))
        update.nama = request.form['nama']
        update.telp = request.form['telp']
        update.no_sk = request.form['no-sk']

        db.session.commit()
        flash("Data berhasil diubah")

        return redirect(url_for('main.input_data_kelompok_tani'))


@ main.route("/input-data/data-kelompok-tani/delete", methods=['GET', 'POST'])
@ login_required
def input_data_kelompok_tani_delete():
    id_poktan = request.form['id_poktan']
    delete = Kelompok_Tani.query.get(id_poktan)

    db.session.delete(delete)
    db.session.commit()
    flash("Data berhasil dihapus")

    return redirect(url_for('main.input_data_kelompok_tani'))


@ main.route("/input-data/data-individu-petani")
@ login_required
def input_data_individu_petani():
    active = 'active'

    image = None
    if current_user.foto:
        image = base64.b64encode(current_user.foto).decode('ascii')  

    provinsi = Provinsi.query.all()
    all_data = Petani.query.all()

    if all_data:
        for foto in all_data:
            foto_petani = base64.b64encode(foto.foto).decode('ascii')
        return render_template("input-data-individu-petani.html", foto_petani=foto_petani, foto=image, name=current_user.nama, level=current_user.level, input_data_individu_petani_navbar=active, input_data_pertanian_navbar=active, individu_petani=all_data, provinsi=provinsi)
    return render_template("input-data-individu-petani.html", foto=image, name=current_user.nama, level=current_user.level, input_data_individu_petani_navbar=active, input_data_pertanian_navbar=active, individu_petani=all_data, provinsi=provinsi)


@ main.route("/input-data/data-kelompok-tani/live-search", methods=['GET', 'POST'])
@ login_required
def live_search_data_kelompok_tani():
    if request.method == 'POST':
        id = request.form['desa_response']
        poktan = Kelompok_Tani.query.filter(Kelompok_Tani.id_desa.like(id))
    return jsonify({'htmlresponse': render_template('data-kelompok-tani-response.html', kelompok_tani=poktan)})


@ main.route("/input-data/data-individu-petani/add", methods=['POST'])
@ login_required
def input_data_individu_petani_add():
    if request.method == 'POST':
        id_desa = request.form['desa']
        id_poktan = request.form['poktan']
        id_petani = request.form['id_petani']
        id = id_desa+id_petani
        nama = request.form['nama']
        nik = request.form['nik']
        no_kk = request.form['no_kk']
        no_ktp = request.form['no_ktp']
        tempat_lahir = request.form['tempat_lahir']
        tanggal_lahir = request.form['tanggal_lahir']
        telp = request.form['telp']
        alamat = request.form['alamat']
        foto = request.files['foto']
        foto = foto.read()
        pin_koordinat = request.form['pin_koordinat']

        petani = Petani.query.filter_by(id_petani=id).first()
        if petani:
            flash('ID telah digunakan')
            return redirect(url_for('main.input_data_individu_petani'))

        add_Data = Petani(id_petani=id, id_poktan=id_poktan, nama=nama, nik=nik, no_kk=no_kk, no_ktp=no_ktp, tempat_lahir=tempat_lahir, tanggal_lahir=tanggal_lahir, telp=telp, alamat=alamat, foto=foto, pin_kordinat=pin_koordinat)

        db.session.add(add_Data)
        db.session.commit()
        flash("Data berhasil ditambahkan")

        return redirect(url_for('main.input_data_individu_petani'))


@ main.route("/input-data/data-individu-petani/update", methods=['GET', 'POST'])
@ login_required
def input_data_individu_petani_update():
    if request.method == 'POST':
        update = Petani.query.get(request.form.get('id_petani'))
        update.nama = request.form['nama']
        update.nik = request.form['nik']
        update.no_kk = request.form['no_kk']
        update.no_ktp = request.form['no_ktp']
        update.tempat_lahir = request.form['tempat_lahir']
        update.tanggal_lahir = request.form['tanggal_lahir']
        update.telp = request.form['telp']
        update.alamat = request.form['alamat']
        foto = request.files['foto']
        if foto:
            foto = foto.read()
            update.foto = foto
        update.pin_kordinat = request.form['pin_koordinat']

        db.session.commit()
        flash("Data berhasil diubah")

        return redirect(url_for('main.input_data_individu_petani'))


@ main.route("/input-data/data-individu-petani/delete", methods=['GET', 'POST'])
@ login_required
def input_data_individu_petani_delete():
    id_petani = request.form['id_petani']
    delete = Petani.query.get(id_petani)

    db.session.delete(delete)
    db.session.commit()
    flash("Data berhasil dihapus")

    return redirect(url_for('main.input_data_individu_petani'))


@ main.route("/input-data/data-individu-lahan")
@ login_required
def input_data_individu_lahan():
    active = 'active'

    image = None
    if current_user.foto:
        image = base64.b64encode(current_user.foto).decode('ascii')  

    provinsi = Provinsi.query.all()
    all_data = Lahan.query.all()

    if all_data:
        for foto in all_data:
            foto_lahan = base64.b64encode(foto.foto).decode('ascii')
        return render_template("input-data-individu-lahan.html", foto_lahan=foto_lahan, foto=image, name=current_user.nama, level=current_user.level, input_data_individu_lahan_navbar=active, input_data_pertanian_navbar=active, individu_lahan=all_data, provinsi=provinsi)
    return render_template("input-data-individu-lahan.html", foto=image, name=current_user.nama, level=current_user.level, input_data_individu_lahan_navbar=active, input_data_pertanian_navbar=active, individu_lahan=all_data, provinsi=provinsi)


@ main.route("/input-data/data-individu-petani/live-search", methods=['GET', 'POST'])
@ login_required
def live_search_data_petani():
    if request.method == 'POST':
        id = request.form['poktan_response']
        petani = Petani.query.filter(Petani.id_poktan.like(id))
    return jsonify({'htmlresponse': render_template('data-petani-response.html', petani=petani)})


@ main.route("/input-data/data-individu-lahan/add", methods=['POST'])
@ login_required
def input_data_individu_lahan_add():
    if request.method == 'POST':
        id_desa = request.form['desa']
        id_lahan = request.form['lahan']
        id_petani = request.form['petani']
        id = id_desa+id_lahan
        alamat = request.form['alamat']
        luas = request.form['luas']
        datetime = request.form['datetime']
        foto = request.files['foto']
        foto = foto.read()
        file = request.files['json']

        lahan = Lahan.query.filter_by(id_lahan=id).first()
        if lahan:
            flash('ID telah digunakan')
            return redirect(url_for('main.input_data_individu_lahan'))

        json = "{}.json".format(id)
        extfile = file.filename.rsplit('.', 1)[1].lower()

        file.save(os.path.join("app/static/json/temporary", "{}.{}".format(id, extfile)))
        patoolib.extract_archive("app/static/json/temporary/{}.{}".format(id, extfile), outdir="app/static/json/temporary/")

        dir = 'app/static/json/temporary'
        search_shp = [f for f in os.listdir(dir) if f.endswith(".shp")]

        gjson = gpd.read_file("app/static/json/temporary/{}".format(search_shp[0]))
        gjson.to_file("app/static/json/temporary/{}".format(json), driver='GeoJSON')
        gjson = gjson.to_json()

        add_Data = Lahan(id_lahan=id, id_petani=id_petani, alamat=alamat, luas=luas, datetime=datetime, foto=foto, polygon=gjson)

        db.session.add(add_Data)
        db.session.commit()

        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))

        flash("Data berhasil ditambahkan")

        return redirect(url_for('main.input_data_individu_lahan'))


@ main.route("/input-data/data-individu-lahan/update", methods=['GET', 'POST'])
@ login_required
def input_data_individu_lahan_update():
    if request.method == 'POST':
        update = Lahan.query.get(request.form.get('id_lahan'))
        update.alamat = request.form['alamat']
        update.luas = request.form['luas']
        update.datetime = request.form['datetime']
        foto = request.files['foto']
        if foto:
            foto = foto.read()
            update.foto = foto
        file = request.files['json']

        if file:
            json = "{}.json".format(id)
            extfile = file.filename.rsplit('.', 1)[1].lower()

            file.save(os.path.join("app/static/json/temporary", "{}.{}".format(id, extfile)))
            patoolib.extract_archive("app/static/json/temporary/{}.{}".format(id, extfile), outdir="app/static/json/temporary/")

            dir = 'app/static/json/temporary'
            search_shp = [f for f in os.listdir(dir) if f.endswith(".shp")]

            gjson = gpd.read_file("app/static/json/temporary/{}".format(search_shp[0]))
            gjson.to_file("app/static/json/temporary/{}".format(json), driver='GeoJSON')
            gjson = gjson.to_json()

            update.polygon = gjson

            for f in os.listdir(dir):
                os.remove(os.path.join(dir, f))

        db.session.commit()
        flash("Data berhasil diubah")

        return redirect(url_for('main.input_data_individu_lahan'))


@ main.route("/input-data/data-individu-lahan/delete", methods=['GET', 'POST'])
@ login_required
def input_data_individu_lahan_delete():
    id_lahan = request.form['id_lahan']
    delete = Lahan.query.get(id_lahan)

    db.session.delete(delete)
    db.session.commit()
    flash("Data berhasil dihapus")

    return redirect(url_for('main.input_data_individu_lahan'))


@ main.route("/input-data/data-komoditas")
@ login_required
def input_data_komoditas():
    active = 'active'

    image = None
    if current_user.foto:
        image = base64.b64encode(current_user.foto).decode('ascii')

    all_data = Komoditas.query.all()
    return render_template("input-data-komoditas.html", foto=image, name=current_user.nama, level=current_user.level, input_data_komoditas_navbar=active, input_data_pertanian_navbar=active, komoditas=all_data)


@ main.route("/input-data/data-komoditas/add", methods=['POST'])
@ login_required
def input_data_komoditas_add():
    if request.method == 'POST':
        id = request.form['id']
        nama = request.form['nama']
        vol_sat = request.form['volume-satuan']
        harga = request.form['harga']
        pemulia = request.form['pemulia']
        keterangan = request.form['keterangan']

        komoditas = Komoditas.query.filter_by(id_komoditas=id).first()
        if komoditas:
            flash('ID telah digunakan')
            return redirect(url_for('main.input_data_Komoditas'))

        add_Data = Komoditas(id_komoditas=id, nama=nama, vol_sat=vol_sat, harga=harga, pemulia=pemulia, keterangan=keterangan)

        db.session.add(add_Data)
        db.session.commit()
        flash("Data berhasil ditambahkan")

        return redirect(url_for('main.input_data_komoditas'))


@ main.route("/input-data/data-komoditas/update", methods=['GET', 'POST'])
@ login_required
def input_data_komoditas_update():
    if request.method == 'POST':
        update = Komoditas.query.get(request.form.get('id_komoditas'))
        update.nama = request.form['nama']
        update.vol_sat = request.form['volume-satuan']
        update.harga = request.form['harga']
        update.pemulia = request.form['pemulia']
        update.keterangan = request.form['keterangan']

        db.session.commit()
        flash("Data berhasil diubah")

        return redirect(url_for('main.input_data_komoditas'))


@ main.route("/input-data/data-komoditas/delete", methods=['GET', 'POST'])
@ login_required
def input_data_komoditas_delete():
    id_komoditas = request.form['id_komoditas']
    delete = Komoditas.query.get(id_komoditas)

    db.session.delete(delete)
    db.session.commit()
    flash("Data berhasil dihapus")

    return redirect(url_for('main.input_data_komoditas'))


@ main.route("/input-data/data-pupuk")
@ login_required
def input_data_pupuk():
    active = 'active'

    image = None
    if current_user.foto:
        image = base64.b64encode(current_user.foto).decode('ascii')

    all_data = Pupuk.query.all()
    return render_template("input-data-pupuk.html", foto=image, name=current_user.nama, level=current_user.level, input_data_pupuk_navbar=active, input_data_pertanian_navbar=active, pupuk=all_data)


@ main.route("/input-data/data-pupuk/add", methods=['POST'])
@ login_required
def input_data_pupuk_add():
    if request.method == 'POST':
        id = request.form['id']
        nama = request.form['nama']
        vol_sat = request.form['volume-satuan']
        harga = request.form['harga']
        pemulia = request.form['pemulia']
        keterangan = request.form['keterangan']

        pupuk = Pupuk.query.filter_by(id_pupuk=id).first()
        if pupuk:
            flash('ID telah digunakan')
            return redirect(url_for('main.input_data_pupuk'))

        add_Data = Pupuk(id_pupuk=id, nama=nama, vol_sat=vol_sat, harga=harga, pemulia=pemulia, keterangan=keterangan)

        db.session.add(add_Data)
        db.session.commit()
        flash("Data berhasil ditambahkan")

        return redirect(url_for('main.input_data_pupuk'))


@ main.route("/input-data/data-pupuk/update", methods=['GET', 'POST'])
@ login_required
def input_data_pupuk_update():
    if request.method == 'POST':
        update = Pupuk.query.get(request.form.get('id_pupuk'))
        update.nama = request.form['nama']
        update.vol_sat = request.form['volume-satuan']
        update.harga = request.form['harga']
        update.pemulia = request.form['pemulia']
        update.keterangan = request.form['keterangan']

        db.session.commit()
        flash("Data berhasil diubah")

        return redirect(url_for('main.input_data_pupuk'))


@ main.route("/input-data/data-pupuk/delete", methods=['GET', 'POST'])
@ login_required
def input_data_pupuk_delete():
    id_pupuk = request.form['id_pupuk']
    delete = Pupuk.query.get(id_pupuk)

    db.session.delete(delete)
    db.session.commit()
    flash("Data berhasil dihapus")

    return redirect(url_for('main.input_data_pupuk'))


@ main.route("/input-data/data-hama")
@ login_required
def input_data_hama():
    active = 'active'

    image = None
    if current_user.foto:
        image = base64.b64encode(current_user.foto).decode('ascii')

    all_data = Hama.query.all()
    return render_template("input-data-hama.html", foto=image, name=current_user.nama, level=current_user.level, input_data_hama_navbar=active, input_data_pertanian_navbar=active, hama=all_data)


@ main.route("/input-data/data-hama/add", methods=['POST'])
@ login_required
def input_data_hama_add():
    if request.method == 'POST':
        id = request.form['id']
        nama = request.form['nama']
        vol_sat = request.form['volume-satuan']
        harga = request.form['harga']
        pemulia = request.form['pemulia']
        keterangan = request.form['keterangan']

        hama = Hama.query.filter_by(id_hama=id).first()
        if hama:
            flash('ID telah digunakan')
            return redirect(url_for('main.input_data_hama'))

        add_Data = Hama(id_hama=id, nama=nama, vol_sat=vol_sat, harga=harga, pemulia=pemulia, keterangan=keterangan)

        db.session.add(add_Data)
        db.session.commit()
        flash("Data berhasil ditambahkan")

        return redirect(url_for('main.input_data_hama'))


@ main.route("/input-data/data-hama/update", methods=['GET', 'POST'])
@ login_required
def input_data_hama_update():
    if request.method == 'POST':
        update = Hama.query.get(request.form.get('id_hama'))
        update.nama = request.form['nama']
        update.vol_sat = request.form['volume-satuan']
        update.harga = request.form['harga']
        update.pemulia = request.form['pemulia']
        update.keterangan = request.form['keterangan']

        db.session.commit()
        flash("Data berhasil diubah")

        return redirect(url_for('main.input_data_hama'))


@ main.route("/input-data/data-hama/delete", methods=['GET', 'POST'])
@ login_required
def input_data_hama_delete():
    id_hama = request.form['id_hama']
    delete = Hama.query.get(id_hama)

    db.session.delete(delete)
    db.session.commit()
    flash("Data berhasil dihapus")

    return redirect(url_for('main.input_data_hama'))


@ main.route("/input-data/data-racun")
@ login_required
def input_data_racun():
    active = 'active'

    image = None
    if current_user.foto:
        image = base64.b64encode(current_user.foto).decode('ascii')

    all_data = Racun.query.all()
    return render_template("input-data-racun.html", foto=image, name=current_user.nama, level=current_user.level, input_data_racun_navbar=active, input_data_pertanian_navbar=active, racun=all_data)


@ main.route("/input-data/data-racun/add", methods=['POST'])
@ login_required
def input_data_racun_add():
    if request.method == 'POST':
        id = request.form['id']
        nama = request.form['nama']
        vol_sat = request.form['volume-satuan']
        harga = request.form['harga']
        pemulia = request.form['pemulia']
        keterangan = request.form['keterangan']

        racun = Racun.query.filter_by(id_racun=id).first()
        if racun:
            flash('ID telah digunakan')
            return redirect(url_for('main.input_data_racun'))

        add_Data = Racun(id_racun=id, nama=nama, vol_sat=vol_sat, harga=harga, pemulia=pemulia, keterangan=keterangan)

        db.session.add(add_Data)
        db.session.commit()
        flash("Data berhasil ditambahkan")

        return redirect(url_for('main.input_data_racun'))


@ main.route("/input-data/data-racun/update", methods=['GET', 'POST'])
@ login_required
def input_data_racun_update():
    if request.method == 'POST':
        update = Racun.query.get(request.form.get('id_racun'))
        update.nama = request.form['nama']
        update.vol_sat = request.form['volume-satuan']
        update.harga = request.form['harga']
        update.pemulia = request.form['pemulia']
        update.keterangan = request.form['keterangan']

        db.session.commit()
        flash("Data berhasil diubah")

        return redirect(url_for('main.input_data_racun'))


@ main.route("/input-data/data-racun/delete", methods=['GET', 'POST'])
@ login_required
def input_data_racun_delete():
    id_racun = request.form['id_racun']
    delete = Racun.query.get(id_racun)

    db.session.delete(delete)
    db.session.commit()
    flash("Data berhasil dihapus")

    return redirect(url_for('main.input_data_racun'))


@ main.route("/input-data/data-log-tanam")
@ login_required
def input_data_log_tanam():
    active = 'active'

    image = None
    if current_user.foto:
        image = base64.b64encode(current_user.foto).decode('ascii')

    all_data = Log_Tanam.query.all()
    provinsi = Provinsi.query.all()
    komoditas = Komoditas.query.all()
    return render_template("input-data-log-tanam.html", foto=image, name=current_user.nama, level=current_user.level, input_data_log_tanam_navbar=active, input_data_log_pertanian_navbar=active, input_data_pertanian_navbar=active, log_tanam=all_data, provinsi=provinsi, komoditas=komoditas)


@ main.route("/input-data/data-individu-lahan/live-search", methods=['GET', 'POST'])
@ login_required
def live_search_data_lahan():
    if request.method == 'POST':
        id = request.form['petani_response']
        lahan = Lahan.query.filter(Lahan.id_petani.like(id))
    return jsonify({'htmlresponse': render_template('data-lahan-response.html', lahan=lahan)})


@ main.route("/input-data/data-log-tanam/add", methods=['POST'])
@ login_required
def input_data_log_tanam_add():
    if request.method == 'POST':
        id_lahan = request.form['lahan']
        id_komoditas = request.form['komoditas']
        mulai = request.form['mulai']
        selesai = request.form['selesai']
        produksi = request.form['produksi']

        add_Data = Log_Tanam(id_lahan=id_lahan, id_komoditas=id_komoditas, tgl_mulai=mulai, tgl_selesai=selesai, total_produksi=produksi)

        db.session.add(add_Data)
        db.session.commit()
        flash("Data berhasil ditambahkan")

        return redirect(url_for('main.input_data_log_tanam'))


@ main.route("/input-data/data-log-tanam/update", methods=['GET', 'POST'])
@ login_required
def input_data_log_tanam_update():
    if request.method == 'POST':
        update = Log_Tanam.query.get(request.form.get('id_log'))
        update.tgl_mulai = request.form['mulai']
        update.tgl_selesai = request.form['selesai']
        update.total_produksi = request.form['produksi']

        db.session.commit()
        flash("Data berhasil diubah")

        return redirect(url_for('main.input_data_log_tanam'))


@ main.route("/input-data/data-log-tanam/delete", methods=['GET', 'POST'])
@ login_required
def input_data_log_tanam_delete():
    id_log = request.form['id_log']
    delete = Log_Tanam.query.get(id_log)

    db.session.delete(delete)
    db.session.commit()
    flash("Data berhasil dihapus")

    return redirect(url_for('main.input_data_log_tanam'))


@ main.route("/input-data/data-log-pupuk-pertanian")
@ login_required
def input_data_log_pupuk_pertanian():
    active = 'active'

    image = None
    if current_user.foto:
        image = base64.b64encode(current_user.foto).decode('ascii')

    all_data = Detail_Log_Tanam_Pupuk.query.all()
    provinsi = Provinsi.query.all()
    pupuk = Pupuk.query.all()
    return render_template("input-data-log-pupuk-pertanian.html", foto=image, name=current_user.nama, level=current_user.level, input_data_log_pupuk_pertanian_navbar=active, input_data_log_pertanian_navbar=active, input_data_pertanian_navbar=active, log_pupuk_pertanian=all_data, provinsi=provinsi, pupuk=pupuk)


@ main.route("/input-data/data-log-tanam/live-search", methods=['GET', 'POST'])
@ login_required
def live_search_data_log_tanam():
    if request.method == 'POST':
        id = request.form['lahan_response']
        log_tanam = Log_Tanam.query.filter(Log_Tanam.id_lahan.like(id))
    return jsonify({'htmlresponse': render_template('data-log-tanam-response.html', log_tanam=log_tanam)})


@ main.route("/input-data/data-log-pupuk-pertanian/add", methods=['POST'])
@ login_required
def input_data_log_pupuk_pertanian_add():
    if request.method == 'POST':
        id_log = request.form['log']
        id_pupuk = request.form['pupuk']

        add_Data = Detail_Log_Tanam_Pupuk(id_log=id_log, id_pupuk=id_pupuk)

        db.session.add(add_Data)
        db.session.commit()
        flash("Data berhasil ditambahkan")

        return redirect(url_for('main.input_data_log_pupuk_pertanian'))


@ main.route("/input-data/data-log-pupuk-pertanian/update", methods=['GET', 'POST'])
@ login_required
def input_data_log_pupuk_pertanian_update():
    if request.method == 'POST':
        update = Detail_Log_Tanam_Pupuk.query.get(request.form.get('id_detaillog'))
        update.id_pupuk = request.form['pupuk']

        db.session.commit()
        flash("Data berhasil diubah")

        return redirect(url_for('main.input_data_log_pupuk_pertanian'))


@ main.route("/input-data/data-log-pupuk-pertanian/delete", methods=['GET', 'POST'])
@ login_required
def input_data_log_pupuk_pertanian_delete():
    id_detaillog = request.form['id_detaillog']
    delete = Detail_Log_Tanam_Pupuk.query.get(id_detaillog)

    db.session.delete(delete)
    db.session.commit()
    flash("Data berhasil dihapus")

    return redirect(url_for('main.input_data_log_pupuk_pertanian'))


@ main.route("/input-data/data-log-hama-pertanian")
@ login_required
def input_data_log_hama_pertanian():
    active = 'active'

    image = None
    if current_user.foto:
        image = base64.b64encode(current_user.foto).decode('ascii')

    all_data = Detail_Log_Tanam_Hama.query.all()
    provinsi = Provinsi.query.all()
    hama = Hama.query.all()
    return render_template("input-data-log-hama-pertanian.html", foto=image, name=current_user.nama, level=current_user.level, input_data_log_hama_pertanian_navbar=active, input_data_log_pertanian_navbar=active, input_data_pertanian_navbar=active, log_hama_pertanian=all_data, provinsi=provinsi, hama=hama)


@ main.route("/input-data/data-log-hama-pertanian/add", methods=['POST'])
@ login_required
def input_data_log_hama_pertanian_add():
    if request.method == 'POST':
        id_log = request.form['log']
        id_hama = request.form['hama']

        add_Data = Detail_Log_Tanam_Hama(id_log=id_log, id_hama=id_hama)

        db.session.add(add_Data)
        db.session.commit()
        flash("Data berhasil ditambahkan")

        return redirect(url_for('main.input_data_log_hama_pertanian'))


@ main.route("/input-data/data-log-hama-pertanian/update", methods=['GET', 'POST'])
@ login_required
def input_data_log_hama_pertanian_update():
    if request.method == 'POST':
        update = Detail_Log_Tanam_Hama.query.get(request.form.get('id_detaillog'))
        update.id_hama = request.form['hama']

        db.session.commit()
        flash("Data berhasil diubah")

        return redirect(url_for('main.input_data_log_hama_pertanian'))


@ main.route("/input-data/data-log-hama-pertanian/delete", methods=['GET', 'POST'])
@ login_required
def input_data_log_hama_pertanian_delete():
    id_detaillog = request.form['id_detaillog']
    delete = Detail_Log_Tanam_Hama.query.get(id_detaillog)

    db.session.delete(delete)
    db.session.commit()
    flash("Data berhasil dihapus")

    return redirect(url_for('main.input_data_log_hama_pertanian'))


@ main.route("/input-data/data-log-racun-pertanian")
@ login_required
def input_data_log_racun_pertanian():
    active = 'active'

    image = None
    if current_user.foto:
        image = base64.b64encode(current_user.foto).decode('ascii')

    all_data = Detail_Log_Tanam_Racun.query.all()
    provinsi = Provinsi.query.all()
    racun = Racun.query.all()
    return render_template("input-data-log-racun-pertanian.html", foto=image, name=current_user.nama, level=current_user.level, input_data_log_racun_pertanian_navbar=active, input_data_log_pertanian_navbar=active, input_data_pertanian_navbar=active, log_racun_pertanian=all_data, provinsi=provinsi, racun=racun)


@ main.route("/input-data/data-log-racun-pertanian/add", methods=['POST'])
@ login_required
def input_data_log_racun_pertanian_add():
    if request.method == 'POST':
        id_log = request.form['log']
        id_racun = request.form['racun']

        add_Data = Detail_Log_Tanam_Racun(id_log=id_log, id_racun=id_racun)

        db.session.add(add_Data)
        db.session.commit()
        flash("Data berhasil ditambahkan")

        return redirect(url_for('main.input_data_log_racun_pertanian'))


@ main.route("/input-data/data-log-racun-pertanian/update", methods=['GET', 'POST'])
@ login_required
def input_data_log_racun_pertanian_update():
    if request.method == 'POST':
        update = Detail_Log_Tanam_Racun.query.get(request.form.get('id_detaillog'))
        update.id_racun = request.form['racun']

        db.session.commit()
        flash("Data berhasil diubah")

        return redirect(url_for('main.input_data_log_racun_pertanian'))


@ main.route("/input-data/data-log-racun-pertanian/delete", methods=['GET', 'POST'])
@ login_required
def input_data_log_racun_pertanian_delete():
    id_detaillog = request.form['id_detaillog']
    delete = Detail_Log_Tanam_Racun.query.get(id_detaillog)

    db.session.delete(delete)
    db.session.commit()
    flash("Data berhasil dihapus")

    return redirect(url_for('main.input_data_log_racun_pertanian'))