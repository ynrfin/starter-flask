from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_mail import Message

from app.user.models import User
from app.extensions import login_manager, bcrypt, db, mail
from flask_login import login_user
from .forms import RegisterForm, LoginForm, ForgotPasswordForm
from .forms import ResetPasswordForm
ResetPasswordForm
from pprint import pprint
from itsdangerous import URLSafeSerializer
from app.config import Config

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

@bp.route('/forgot-password', methods=['POST', 'GET'])
def forgot_password():
    form = ForgotPasswordForm()
    if(form.validate_on_submit()):
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            s = URLSafeSerializer(Config.SECRET_KEY)
            user.reset_password_token = s.dumps([user.id, user.password])
            db.session.commit()
            reset_link= url_for('public.reset_password',
                    token=user.reset_password_token)
            email_message = '''Hello, you have requested a reset password token.
            Ignore this if you do not think you requested one.
            <a href="{}"> {}</a>'''
            email_message = email_message.format(reset_link,
                    reset_link)
            return email_message
            msg = Message(email_message, sender="yourapp@mail.com", recipients=['mygmart1@gmail.com'])
            mail.send(msg)
            flash("We have send a link to reset your password. Please check your email")

            return redirect(url_for('public.index'))
        else:
            flash('no user found')
            return redirect(url_for('public.index'))
    return render_template('forgot-password.html', form=form)

@bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password(token=None):
    token = request.args.get('token') or None
    if token is not None:
        user = User.query.filter_by(reset_password_token=token).first()
        if user is not None:
            form = ResetPasswordForm()
            if form.validate_on_submit():
                user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user.reset_password_token = None
                db.session.commit()
                flash("Password Changed")
                return redirect(url_for('public.index'))
            return render_template('reset-password.html', form=form,
                username= user.username)
        flash('Token not found, please request new token')
        return redirect(url_for('public.index'))
    return 'no token'
