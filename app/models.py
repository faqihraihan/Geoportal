from flask_login import UserMixin
from datetime import datetime
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.VARCHAR(200), unique=True)
    password = db.Column(db.VARCHAR(200))
    nama = db.Column(db.VARCHAR(200))
    telp = db.Column(db.VARCHAR(200))
    lvl = db.Column(db.Integer)
    img = db.Column(db.LargeBinary(length=(2**32)-1))
    waktu = db.Column(db.DateTime, default=datetime.now())


class Provinsi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.VARCHAR(200))
    waktu = db.Column(db.DateTime, default=datetime.now())
    kab = db.relationship("Kabupaten", backref="provinsi")


class Kabupaten(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_prov = db.Column(db.Integer, db.ForeignKey('provinsi.id'))
    nama = db.Column(db.VARCHAR(200))
    waktu = db.Column(db.DateTime, default=datetime.now())
    kec = db.relationship("Kecamatan", backref="kabupaten")


class Kecamatan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_kab = db.Column(db.Integer, db.ForeignKey('kabupaten.id'))
    nama = db.Column(db.VARCHAR(200))
    waktu = db.Column(db.DateTime, default=datetime.now())
    desa = db.relationship("Desa", backref="kecamatan")


class Desa(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    id_kec = db.Column(db.Integer, db.ForeignKey('kecamatan.id'))
    nama = db.Column(db.VARCHAR(200))
    waktu = db.Column(db.DateTime, default=datetime.now())
    kel_tani = db.relationship("Kelompok_Tani", backref="desa")
    gapoktan = db.relationship("Gapoktan", backref="desa")
    peta_desa = db.relationship("Peta_Desa", backref="desa")


class Bibit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.VARCHAR(200))
    vol_sat = db.Column(db.Integer)
    harga = db.Column(db.Integer)
    pemulia = db.Column(db.VARCHAR(200))
    waktu = db.Column(db.DateTime, default=datetime.now())


class Pupuk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.VARCHAR(200))
    vol_sat = db.Column(db.Integer)
    harga = db.Column(db.Integer)
    pemulia = db.Column(db.VARCHAR(200))
    waktu = db.Column(db.DateTime, default=datetime.now())


class Gapoktan(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    id_desa = db.Column(db.BigInteger, db.ForeignKey('desa.id'))
    nama = db.Column(db.VARCHAR(200))
    ketua = db.Column(db.VARCHAR(200))
    telp = db.Column(db.VARCHAR(200))
    no_sk = db.Column(db.VARCHAR(200))
    waktu = db.Column(db.DateTime, default=datetime.now())


class Kelompok_Tani(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    id_desa = db.Column(db.BigInteger, db.ForeignKey('desa.id'))
    nama = db.Column(db.VARCHAR(200))
    telp = db.Column(db.VARCHAR(200))
    no_sk = db.Column(db.VARCHAR(200))
    waktu = db.Column(db.DateTime, default=datetime.now())


class Peta_Desa(db.Model):
    id = db.Column(db.BigInteger, db.ForeignKey('desa.id'), primary_key=True)
    nama = db.Column(db.VARCHAR(200))
    json = db.Column(db.JSON)
    waktu = db.Column(db.DateTime, default=datetime.now())