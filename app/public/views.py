from flask import Blueprint, render_template, redirect, url_for
from flask_mail import Message

from app.user.models import User
from app.extensions import login_manager, bcrypt, db, mail
from flask_login import login_user
from .forms import RegisterForm, LoginForm
import pprint

bp = Blueprint('public', __name__, template_folder='templates/public')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form =  RegisterForm();
    if(form.validate_on_submit()):
        new_account = User()
        new_account.fullname = form.name.data;
        new_account.username = form.username.data;
        new_account.password= bcrypt.generate_password_hash(
                form.password.data).decode('utf-8');
        db.session.add(new_account)
        db.session.commit()
        return 'account made'
    
    return render_template('register.html', form=form)

@bp.route('/login', methods=['POST', "GET"])
def login():
    form = LoginForm()
    if(form.validate_on_submit()):
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            if(bcrypt.check_password_hash(user.password,
                form.password.data)):
                login_user(user)
                return redirect(url_for('public.index'))
    return render_template('login.html', form=form)

