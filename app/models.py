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
    id_desa = db.Column(db.BIGINT, primary_key=True)
    nama_desa = db.Column(db.VARCHAR(200))

class Gapoktan(db.Model):
    id_gapoktan = db.Column(db.Integer, primary_key=True)
    id_desa = db.Column(db.BIGINT)
    nama_gapoktan = db.Column(db.VARCHAR(200))
    alamat_gapoktan = db.Column(db.VARCHAR(200))
    telepon_gapoktan = db.Column(db.VARCHAR(200))
    tahun_terbentuk_gapoktan = db.Column(db.VARCHAR(200))

class Komoditi(db.Model):
    __tablename__ = 'komoditi'
    id_komoditi = db.Column(db.Integer, primary_key=True)
    nama_komoditi = db.Column(db.VARCHAR(50))