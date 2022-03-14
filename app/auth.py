from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Email atau Password salah')
        return redirect(url_for('auth.login'))

    login_user(user)

    return redirect(url_for('main.dashboard'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    name = request.form.get('name')
    nohp = request.form.get('nohp')
    email = request.form.get('email')
    password = request.form.get('password')
    repassword = request.form.get('repassword')

    user = User.query.filter_by(email=email).first()

    admin = User.query.filter_by(lvl='1').first()
    if not admin:
        lvl = "1"
    else:
        lvl = "5"

    if user: 
        flash('Email telah digunakan')
        return redirect(url_for('auth.signup'))

    if password != repassword:
        flash(u'Password berbeda', 'pass-error')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, nama=name, nohp = nohp, password=generate_password_hash(password, method='sha256'), lvl=lvl)

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@auth.route("/input-data/data-user")
@login_required
def input_data_user():
    active = 'active'
    all_data = User.query.all()
    return render_template("input-data-user.html", name=current_user.nama, input_data_user_navbar=active, user=all_data)

@auth.route("/input-data/data-user/add", methods = ['POST'])
@login_required
def input_data_user_add():
    if request.method == 'POST':
        nama = request.form['name']
        email = request.form['email']
        nohp = request.form['nohp']
        password = request.form['password']
        lvl = request.form['level']
 
        add_Data = User(nama=nama, email=email, nohp=nohp, password=generate_password_hash(password, method='sha256'), lvl=lvl)
        
        db.session.add(add_Data)
        db.session.commit()
        flash("Data telah ditambahkan")
 
        return redirect(url_for('auth.input_data_user'))

@auth.route("/input-data/data-user/update", methods = ['GET', 'POST'])
@login_required
def input_data_user_update():
    if request.method == 'POST':
        update = User.query.get(request.form.get('id'))
 
        update.nama = request.form['name']
        update.email = request.form['email']
        update.nohp = request.form['nohp']
        update.lvl = request.form['level']
 
        db.session.commit()
        flash("Data telah diubah")
 
        return redirect(url_for('auth.input_data_user'))

@auth.route("/input-data/data-user/delete/<id>/", methods = ['GET', 'POST'])
@login_required
def input_data_user_delete(id):
    delete = User.query.get(id)
    db.session.delete(delete)
    db.session.commit()
    flash("Data telah dihapus")
 
    return redirect(url_for('auth.input_data_user'))