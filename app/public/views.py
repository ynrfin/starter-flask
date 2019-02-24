from flask import Blueprint, render_template

from app.user.models import User
from app.extensions import login_manager, bcrypt, db
from .forms import RegisterForm
import pprint

bp = Blueprint('public', __name__, template_folder='templates/public')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form =  RegisterForm();
    if(form.validate_on_submit()):
        new_account = User()
        new_account.fullname = form.name.data;
        new_account.username = form.username.data;
        new_account.password= bcrypt.generate_password_hash(form.password.data);
        db.session.add(new_account)
        db.session.commit()
        return new_account.id
    
    return render_template('register.html', form=form)
