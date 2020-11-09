from flask_login import UserMixin
from sqlalchemy.sql.elements import False_
from werkzeug.security import check_password_hash, generate_password_hash
from app import db, login_manager
from datetime import datetime

# User class for each individual user
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True} 

    _id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    fullname = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    family_id = db.Column(db.Integer, db.ForeignKey('family._id'))

    family = db.relationship("Family", back_populates="users")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def check_family_password(self, family_name, family_password):
        family = Family.query.filter_by(name=family_name).first()
        if family is not None:
            return family.check_password(family_password)

    def set_family_id(self, family_name):
        family = Family.query.filter_by(name=family_name).first()
        family.users.append(self)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def get_id(self):
        return (self._id)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# Family class for each family which can have several users
class Family(db.Model):
    __tablename__ = 'family'
    __table_args__ = {'extend_existing': True} 

    _id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))

    users = db.relationship("User", back_populates="family")
    lists = db.relationship("List", back_populates="family")

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

# Lists class for lists which belong to one family
class List(db.Model):
    __tablename__='list'
    __table_args__ = {'extend_existing': True} 

    _id = db.Column(db.Integer, primary_key=True, unique=True)
    category = db.Column(db.String(120))
    family_id = db.Column(db.Integer, db.ForeignKey("family._id"))
    
    family = db.relationship("Family", back_populates="lists")
    items = db.relationship("Item", back_populates="list")
    
    def get_id(self):
        return self._id

    def set_family_id(self, family_name):
        family = Family.query.filter_by(name=family_name).first()
        self.family_id = family._id

# Items class for items which belong to one list
class Item(db.Model):
    __tablename__ = 'item'
    __table_args__ = {'extend_existing': True} 

    _id = db.Column(db.Integer, primary_key=True, unique=True)
    value = db.Column(db.String(120))
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    list_id = db.Column(db.Integer, db.ForeignKey("list._id"))

    list = db.relationship("List", back_populates="items")




