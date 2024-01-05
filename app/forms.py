from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email

class CalgotForm(FlaskForm):
    nama_lengkap = StringField('Nama Lengkap', validators=[DataRequired('Isi Nama Lengkap')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    nomor_wa = StringField('Nomor Whatsapp', validators=[DataRequired()])
    asal_kampus = StringField('Asal Kampus', validators=[DataRequired()])
    bukti_tf = StringField('Nama File Foto', default="tidak_ada.jpg")
    bukti_follow = StringField('Nama File Foto', default="tidak_ada.jpg")
