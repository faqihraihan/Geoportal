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
    kab = db.relationship("Kabupaten", backref="provinsi")
    kec = db.relationship("Kecamatan", backref="provinsi")
    desa = db.relationship("Desa", backref="provinsi")

class Kabupaten(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_prov = db.Column(db.Integer, db.ForeignKey('provinsi.id'))
    id_kab = db.Column(db.VARCHAR(200))
    nama = db.Column(db.VARCHAR(200))
    kec = db.relationship("Kecamatan", backref="kabupaten")
    desa = db.relationship("Desa", backref="kabupaten")

class Kecamatan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_prov = db.Column(db.Integer, db.ForeignKey('provinsi.id'))
    id_kab = db.Column(db.Integer, db.ForeignKey('kabupaten.id'))
    id_kec = db.Column(db.VARCHAR(200))
    nama = db.Column(db.VARCHAR(200))
    desa = db.relationship("Desa", backref="kecamatan")

class Desa(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    id_prov = db.Column(db.Integer, db.ForeignKey('provinsi.id'))
    id_kab = db.Column(db.Integer, db.ForeignKey('kabupaten.id'))
    id_kec = db.Column(db.Integer, db.ForeignKey('kecamatan.id'))
    id_desa = db.Column(db.VARCHAR(200))
    nama = db.Column(db.VARCHAR(200))

class Kelompok_Tani(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    nama = db.Column(db.VARCHAR(200))
    no_sk = db.Column(db.VARCHAR(200)) 

class Peta_Desa(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    nama = db.Column(db.VARCHAR(200))
    json = db.Column(db.JSON) 