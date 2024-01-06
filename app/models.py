from app import db, login
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(UserMixin, db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True)
    password_hash = Column(String(128))
    def __repr__(self):
        return f'<Admin {self.username}'
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return Admin.query.get(int(id))


class User(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nama_lengkap = Column(String(64))
    email = Column(String(64), unique=True)
    nomor_wa = Column(String(20), unique=True)
    asal_kampus = Column(String(64))
    bukti_tf = Column(String(64), default="tidak_ada.jpg")
    bukti_follow = Column(String(64), default="tidak_ada.jpg")
    status = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.utcnow)
    __table_args__ = (UniqueConstraint('nomor_wa', name='unique_nomor_wa'), UniqueConstraint('email',name='unique_email'))
    def __repr__(self):
        return f"<User {self.nama_lengkap}"

