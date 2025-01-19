from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import Admin, Election, User, Vote  # Ensure all required models are imported
from extensions import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validation
        if not full_name or not email or not password:
            flash("All fields are required!", "error")
        elif password != confirm_password:
            flash("Passwords do not match!", "error")
        elif Admin.query.filter_by(email=email).first():
            flash("Email already exists!", "error")
        else:
            # Hash password and store admin
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_admin = Admin(full_name=full_name, email=email, password=hashed_password)
            db.session.add(new_admin)
            db.session.commit()
            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for('admin.admin_login'))

    return render_template('admin_register.html')

@admin_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        admin = Admin.query.filter_by(email=email).first()

        if not admin or not check_password_hash(admin.password, password):
            flash("Invalid email or password!", "error")
        else:
            session['admin_id'] = admin.id  # Set session
            flash("Login successful!", "success")
            return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin_login.html')

@admin_bp.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        flash("Please log in first.", "error")
        return redirect(url_for('admin.admin_login'))

    # Render the dashboard with relevant stats
    users_count = User.query.count()
    elections_count = Election.query.count()
    votes_count = Vote.query.count()  # Correctly counts all rows in the Vote table
    return render_template('admin_dashboard.html', users_count=users_count, elections_count=elections_count, votes_count=votes_count)

@admin_bp.route('/admin/elections', methods=['GET', 'POST'])
def manage_elections():
    if 'admin_id' not in session:
        flash("Please log in first.", "error")
        return redirect(url_for('admin.admin_login'))

    if request.method == 'POST':
        # Logic to create or edit elections
        name = request.form.get('name')
        date_str = request.form.get('date')
        status = request.form.get('status', 'Upcoming')
        election_id = request.form.get('election_id')

        # Convert date string to date object
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash("Invalid date format!", "error")
            return redirect(url_for('admin.manage_elections'))

        if election_id:  # Editing an existing election
            election = Election.query.get(election_id)
            if election:
                election.name = name
                election.date = date
                election.status = status
        else:  # Creating a new election
            election = Election(name=name, date=date, status=status)
            db.session.add(election)

        db.session.commit()
        flash("Election saved successfully!", "success")
        return redirect(url_for('admin.manage_elections'))
    
    elections = Election.query.all()
    return render_template('manage_elections.html', elections=elections)

@admin_bp.route('/admin/elections/delete/<int:election_id>', methods=['POST'])
def delete_election(election_id):
    if 'admin_id' not in session:
        flash("Please log in first.", "error")
        return redirect(url_for('admin.admin_login'))

    election = Election.query.get(election_id)
    if election:
        db.session.delete(election)
        db.session.commit()
        flash("Election deleted successfully!", "success")
    else:
        flash("Election not found!", "error")
    
    return redirect(url_for('admin.manage_elections'))

@admin_bp.route('/admin/elections/start/<int:election_id>', methods=['POST'])
def start_election(election_id):
    if 'admin_id' not in session:
        flash("Please log in first.", "error")
        return redirect(url_for('admin.admin_login'))

    election = Election.query.get(election_id)
    if election:
        election.status = 'Ongoing'
        db.session.commit()
        flash("Election started successfully!", "success")
    else:
        flash("Election not found!", "error")
    
    return redirect(url_for('admin.manage_elections'))

@admin_bp.route('/admin/elections/end/<int:election_id>', methods=['POST'])
def end_election(election_id):
    if 'admin_id' not in session:
        flash("Please log in first.", "error")
        return redirect(url_for('admin.admin_login'))

    election = Election.query.get(election_id)
    if election:
        election.status = 'Ended'
        db.session.commit()
        flash("Election ended successfully!", "success")
    else:
        flash("Election not found!", "error")
    
    return redirect(url_for('admin.manage_elections'))
