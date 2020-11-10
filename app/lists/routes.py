from flask import render_template, flash, redirect, url_for, Blueprint
from flask_wtf import form
from .forms import AddItem
from app import db
from app.models import User, Family, List, Item
from flask_login import current_user, login_required, login_user, logout_user

lists = Blueprint('lists', __name__)

@lists.route("/shopping", methods=['GET', 'POST'])
def shopping():
    if current_user.is_authenticated:
        family_id = current_user.family_id
        category = "shopping"
        list_id = List.query.filter_by(family_id=family_id, category=category).first().get_id()
        items = Item.query.filter_by(list_id=list_id)
        form = AddItem()
        if form.validate_on_submit():
            new_item = Item(value=form.value.data, list_id=list_id)
            db.session.add(new_item)
            db.session.commit()
            return redirect(url_for('lists.shopping'))
        return render_template('list.html', title='Shopping List', list="shopping", items=items, form=form)
    else:
        redirect(url_for('auth.login'))

@lists.route("/todo", methods=['GET', 'POST'])
def todo():
    if current_user.is_authenticated:
        family_id = current_user.family_id
        category = "to_do"
        list_id = List.query.filter_by(family_id=family_id, category=category).first().get_id()
        items = Item.query.filter_by(list_id=list_id).all()
        form = AddItem()
        if form.validate_on_submit():
            new_item = Item(value=form.value.data, list_id=list_id)
            db.session.add(new_item)
            db.session.commit()
            return redirect(url_for('lists.todo'))
        return render_template('list.html', title='To-Do List', list="todo", items=items, form=form)
    else:
        redirect(url_for('auth.login'))

@lists.route('/complete/<redirect>/<item_id>', methods=['GET','POST']) 
def complete(redirect, item_id):   
    item = Item.query.filter_by(_id=int(item_id)).first() 
    db.session.delete(item)
    db.session.commit()   
    if redirect == "shopping":
        return redirect(url_for('lists.shopping')) 
    elif redirect == "todo":
        return redirect(url_for('lists.todo'))
    elif redirect == "dashboard":
        return redirect(url_for("auth.dashboard"))


