from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from app import db, login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True} 

    _id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    fullname = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    family_id = db.Column(db.Integer, db.ForeignKey('family._id'))
    items = db.relationship('Item', backref='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def check_family_password(self, family_name, family_password):
        family = Family.query.filter_by(name=family_name).first()
        return family.check_password(family_password)

    def set_family_id(self, family_name):
        family = Family.query.filter_by(name=family_name).first()
        self.family_id = family._id

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def get_id(self):
        return (self._id)

class Family(db.Model):
    __tablename__ = 'family'
    __table_args__ = {'extend_existing': True} 

    _id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    members = db.relationship('User', backref='family')
    lists = db.relationship('List', backref='family')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self._id

    def initialise_lists(self):
        to_do_list = List(category="to_do")
        grocery_list = List(category="shopping")       
        to_do_list.set_family_id(self.name)
        grocery_list.set_family_id(self.name)  
        db.session.add(grocery_list)
        db.session.add(to_do_list)
        db.session.commit()

class List(db.Model):
    __tablename__='list'
    __table_args__ = {'extend_existing': True} 

    _id = db.Column(db.Integer, primary_key=True, unique=True)
    family_id = db.Column(db.Integer, db.ForeignKey('family._id'))
    category = db.Column(db.String(120))
    items = db.relationship('Item', backref='list')

    def set_family_id(self, family_name):
        family = Family.query.filter_by(name=family_name).first()
        self.family_id = family._id

class Item(db.Model):
    __tablename__ = 'item'
    __table_args__ = {'extend_existing': True} 

    _id = db.Column(db.Integer, primary_key=True, unique=True)
    value = db.Column(db.String(120))
    assigned_to = db.Column(db.Integer, db.ForeignKey('user._id'))
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    list_id = db.Column(db.Integer, db.ForeignKey('list._id'))



