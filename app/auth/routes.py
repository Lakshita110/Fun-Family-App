from flask import render_template, flash, redirect, url_for, Blueprint
from .forms import LoginForm, RegisterForm
from flask_login import current_user, login_required, login_user, logout_user
from app import db
from app.models import User, Family, List, Item

auth = Blueprint('auth', __name__)

@auth.route("/landing")
@auth.route("/", methods=['GET'])
def landing():
    return render_template ('landing.html')

@auth.route("/dashboard")
def dashboard():
    if current_user.is_authenticated:
        family_id = current_user.family_id
        shopping_list_id = List.query.filter_by(family_id=family_id, category="shopping").first().get_id()
        shopping_items = Item.query.filter_by(list_id=shopping_list_id).all()
        todo_list_id = List.query.filter_by(family_id=family_id, category="to_do").first().get_id()
        todo_items = Item.query.filter_by(list_id=todo_list_id).all()
        return render_template('dashboard.html', title="Dashboard", todo_items=todo_items, shopping_items=shopping_items)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("You're already logged in.")
        return redirect(url_for('auth.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        flash('Congratulations, you are logged in!')
        return redirect(url_for('auth.dashboard'))
    return render_template('login.html', title='Log In', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("You're already logged in.")
        return redirect(url_for('auth.dashboard'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, fullname=form.fullname.data)
        user.set_password(form.password.data)
        if form.existing_family.data == True:         
            if user.check_family_password(form.family_name.data, form.family_password.data):
                user.set_family_id(form.family_name.data)
                db.session.add(user)
                db.session.commit()
                flash('Congratulations, you are registered!')
                return redirect(url_for('auth.login'))
            else: 
                flash('Invalid family name or password')
                return redirect(url_for('auth.register'))
        elif form.existing_family.data == False:
            family_name = form.family_name.data
            if Family.query.filter_by(family_name=family_name).all() is None:
                family = Family(name=family_name)
                family.set_password(form.family_password.data)
                db.session.add(family)
                db.session.commit()
                family.initialise_lists()
                user.set_family_id(family_name)
                db.session.add(user)
                db.session.commit()
                flash('Congratulations, you are registered!')
                return redirect(url_for('auth.login'))
            else:
                flash('Try using a different family name.')
                return redirect(url_for('auth.register'))
    return render_template('register.html',title='Register', form=form)

@auth.route("/logout", methods=['GET', 'POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("Sucessfully logged out!")
        return redirect(url_for('auth.login'))
    else:
        flash("You're not logged in")
        return redirect(url_for('auth.login'))
