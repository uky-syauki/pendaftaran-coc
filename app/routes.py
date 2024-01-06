from flask import redirect, url_for, render_template, request, jsonify, flash
from flask_login import login_required, login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField

from app import app, db
from app.models import User, Admin
from app.forms import CalgotForm

import os


class LoginForm(FlaskForm):
	username = StringField('Username')
	password = PasswordField('Password')
	submit = SubmitField('Login')


@app.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm()
	if current_user.is_authenticated:
		return redirect(url_for('pendaftar'))
	if form.validate_on_submit():
		user = Admin.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash("Username atau Password Salah!!")
			return redirect(url_for('login'))
		flash("Berhasil Login")
		login_user(user)
		return redirect(url_for('pendaftar'))
	return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route("/")
def index():
    return redirect(url_for("daftar"))


@app.route("/daftar")
def daftar():
	form = CalgotForm()
	return render_template("daftar.html", form=form)


@app.route("/infopendaftar")
def info():
	daftarUser = User.query.all()
	return render_template("info.html", daftarUser=daftarUser)


@app.route("/pendaftar")
@login_required
def pendaftar():
	daftarUser = User.query.all()
	return render_template("pendaftar2.html", daftarUser=daftarUser)


@app.route("/api/update", methods=['GET','POST'])
@login_required
def update():
	try:
		id_user = request.get_json()
		user = User.query.get(id_user.get('idd'))
		print(type(id_user.get('idd')))
		print(user.nama_lengkap)
		if user.status == 1:
			user.status = 0
		else:
			user.status = 1
		db.session.add(user)
		db.session.commit()
		return jsonify({"status":'success'})
	except Exception as e:
		db.session.rollback()
		print(str(e))
		return jsonify({"status":'error'})


@app.route('/api/getData', methods=['GET'])
@login_required
@login_required
def getData():
	daftar_calgot = User.query.all()
	data_jsom = []
	for baris in daftar_calgot:
		data_jsom.append({
			'id':baris.id,
			'nama_lengkap':baris.nama_lengkap,
			'status':baris.status,
			'bukti_tf':baris.bukti_tf[41:],
		})
	return jsonify(data_jsom)


@app.route('/api/postData', methods=['GET','POST'])
def postData():
	print('get')
	nama_lengkap = request.form.get('nama_lengkap')
	arrData = User.query.with_entities(User.nomor_wa, User.email).all()
	# tersedia = "data sudah ada: "
	pesan = {}
	# print(arrData[0])
	for isi in arrData:
		wa = request.form.get('nomor_wa').replace(' ','')
		email = request.form.get('email')
		if wa in isi:
			pesan['nomor wa'] = wa
		if email in isi:
			pesan['email'] = email
	if len(pesan) == 0:
		try:
			photo_tf = request.files['photo_tf']
			photo_follow = request.files['photo_follow']
			nama_lengkap = nama_lengkap.replace(' ','_').replace(',','').replace('.','')
			# if server
			# photo_path = os.path.join("/home/daftarcoconut/marvel012/app/static/foto_calgot", nama_lengkap+'.jpg')
			# if Local
			photo_path_tf = os.path.join("/home/coconutopenclass/mysite/app/static/foto_tf/", nama_lengkap+'.jpg')
			photo_tf.save(photo_path_tf)
			photo_path_follow = os.path.join("/home/coconutopenclass/mysite/app/static/foto_follow/", nama_lengkap+'.jpg')
			photo_follow.save(photo_path_follow)
			add_calgot = User(
				nama_lengkap=request.form.get('nama_lengkap'),
				email=request.form.get('email'),
				nomor_wa=request.form.get('nomor_wa').replace(' ',''),
				asal_kampus=request.form.get('kampus'),
				bukti_tf=photo_path_tf,
				bukti_follow=photo_path_follow,
			)
			db.session.add(add_calgot)
			db.session.commit()
			print(f"Calgot {nama_lengkap} berhasil di daftar")
			return jsonify({'status': 'success'})
		except:
			db.session.rollback()
			return jsonify({'status': 'error exc', 'pesan':pesan})
	else:
		db.session.rollback()
		print(len(pesan) == 0)
		return jsonify({'status': 'error', 'pesan':pesan})

	
