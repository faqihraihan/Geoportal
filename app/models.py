from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.VARCHAR(200), unique=True)
    password = db.Column(db.VARCHAR(200))
    nama = db.Column(db.VARCHAR(200))
    nohp = db.Column(db.VARCHAR(200))
    lvl = db.Column(db.Integer)

class Provinsi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.VARCHAR(200))

class Kabupaten(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.VARCHAR(200))

class Kecamatan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.VARCHAR(200))

class Desa(db.Model):
    id_desa = db.Column(db.Integer, primary_key=True)
    nama_desa = db.Column(db.VARCHAR(200))

class Kelompok_Tani(db.Model):
    kode_poktan = db.Column(db.VARCHAR(200), primary_key=True)
    nama_poktan = db.Column(db.VARCHAR(200))
    no_sk = db.Column(db.VARCHAR(200))