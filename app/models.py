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

class Kabupaten(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_prov = db.Column(db.Integer, db.ForeignKey('provinsi.id'))
    nama = db.Column(db.VARCHAR(200))
    kec = db.relationship("Kecamatan", backref="kabupaten")

class Kecamatan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_kab = db.Column(db.Integer, db.ForeignKey('kabupaten.id'))
    nama = db.Column(db.VARCHAR(200))
    desa = db.relationship("Desa", backref="kecamatan")

class Desa(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    id_kec = db.Column(db.Integer, db.ForeignKey('kecamatan.id'))
    nama = db.Column(db.VARCHAR(200))
    gapoktan = db.relationship("Gapoktan", backref="desa")

class Kelompok_Tani(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    nama = db.Column(db.VARCHAR(200))
    no_sk = db.Column(db.VARCHAR(200)) 

class Gapoktan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_desa = db.Column(db.BigInteger, db.ForeignKey('desa.id'))
    nama = db.Column(db.VARCHAR(200))
    alamat = db.Column(db.VARCHAR(200))
    telepon = db.Column(db.VARCHAR(200))
    tahun_terbentuk = db.Column(db.VARCHAR(200))

class Komoditi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.VARCHAR(200))
    bibit = db.relationship("Bibit", backref="komoditi")
    
class Bibit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_kom = db.Column(db.Integer, db.ForeignKey('komoditi.id'))
    nama = db.Column(db.VARCHAR(200))
    volume = db.Column(db.Integer)
    satuan = db.Column(db.VARCHAR(200))
    harga = db.Column(db.Integer)
    pemulia = db.Column(db.VARCHAR(200))

class Pupuk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.VARCHAR(200))
    volume = db.Column(db.Integer)
    satuan = db.Column(db.VARCHAR(200))
    harga = db.Column(db.Integer)
    pemulia = db.Column(db.VARCHAR(200))