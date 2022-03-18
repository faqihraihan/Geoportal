from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.VARCHAR(200), unique=True)
    password = db.Column(db.VARCHAR(200))
    nama = db.Column(db.VARCHAR(200))
    nohp = db.Column(db.VARCHAR(200))
    lvl = db.Column(db.Integer)
    img = db.Column(db.LargeBinary(length=(2**32)-1))

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
    id = db.Column(db.BigInteger, primary_key=True)
    nama = db.Column(db.VARCHAR(200))

class Kelompok_Tani(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    nama = db.Column(db.VARCHAR(200))
    no_sk = db.Column(db.VARCHAR(200)) 