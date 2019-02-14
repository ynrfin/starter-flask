from flask import Blueprint, render_template

bp = Blueprint('user', __name__)

@bp.route('/')
def index():
    return 'user index'
    return render_template('index')

@bp.route('/create')
def create():
    return 'user create'
