from flask import redirect, url_for, render_template, request, jsonify
from flask_login import login_required, login_user, logout_user, current_user

from app import app, db
from app.models import User
from app.forms import CalgotForm

import os

@app.route("/")
def index():
    return redirect(url_for("daftar"))

@app.route("/daftar")
def daftar():
	form = CalgotForm()
	return render_template("daftar.html", form=form)




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

	
