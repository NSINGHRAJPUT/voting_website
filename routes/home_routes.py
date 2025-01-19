# In home_routes.py
from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return render_template('home.html')

# # In auth_routes.py
# from flask import Blueprint, render_template, request, flash, redirect, url_for
# from werkzeug.security import generate_password_hash
# from models import User, db

# auth_bp = Blueprint('auth', __name__)

# @auth_bp.route('/register', methods=['GET', 'POST'])
# def register():
#     # Your registration logic here
#     pass
