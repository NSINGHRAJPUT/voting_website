from flask import Blueprint, render_template, request, flash, redirect, url_for,session
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from extensions import db

# Define the blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        voter_id = request.form.get('voter_id')

        # Validation
        if not full_name or not email or not password or not voter_id:
            flash("All fields are required!", "error")
        elif password != confirm_password:
            flash("Passwords do not match!", "error")
        elif User.query.filter_by(email=email).first():
            flash("Email already exists!", "error")
        elif User.query.filter_by(voter_id=voter_id).first():
            flash("Voter ID already exists!", "error")
        else:
            # Hash password and store user
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(full_name=full_name, email=email, password=hashed_password, voter_id=voter_id)
            db.session.add(new_user)
            db.session.commit()
            print("Registered User Details:")
            print(f"Full Name: {full_name}")
            print(f"Email: {email}")
            print(f"Voter ID: {voter_id}")
            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/login', methods=["GET", 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(f"Received email: {email}")
        print(f"Received password: {password}")
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash("Invalid email or password!", "error")
        else:
            session['user_id'] = user.id  # Set session
            flash("Login successful!", "success")
            return redirect(url_for('dashboard.dashboard'))

    return render_template('login.html')

@auth_bp.route('/create_vote', methods=['GET', 'POST'])
def create_vote():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')

        new_vote = Vote(title=title, description=description, user_id=session['user_id'])
        db.session.add(new_vote)
        db.session.commit()
        flash('Vote created successfully!', 'success')
        return redirect(url_for('dashboard.dashboard'))

    return render_template('create_vote.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
