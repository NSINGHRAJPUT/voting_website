from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models import Election, Candidate, Vote
from extensions import db

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return render_template('home.html')

@home_bp.route('/elections')
def elections():
    all_elections = Election.query.all()
    return render_template('elections.html', elections=all_elections)

@home_bp.route('/vote/<int:election_id>', methods=['GET', 'POST'])
def vote(election_id):
    election = Election.query.get_or_404(election_id)
    candidates = Candidate.query.filter_by(election_id=election_id).all()
    
    if request.method == 'POST':
        user_email = request.form.get('email')
        candidate_id = request.form.get('candidate_id')
        
        # Check if the user has already voted in this election
        if Vote.query.filter_by(email=user_email, election_id=election_id).first():
            flash('You have already voted in this election.', 'error')
            return redirect(url_for('home.vote', election_id=election_id))
        
        # Record the vote
        vote = Vote(email=user_email, election_id=election_id, candidate_id=candidate_id)
        db.session.add(vote)
        db.session.commit()
        flash('Vote done successfully.', 'success')
        
    return render_template('vote.html', election=election, candidates=candidates)

@home_bp.route('/results/<int:election_id>')
def results(election_id):
    election = Election.query.get_or_404(election_id)
    # Assuming we have a method to get the results
    results = get_election_results(election_id)
    return render_template('results.html', election=election, results=results)

@home_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Process the form data (e.g., save to the database, send an email, etc.)
        flash('Thank you for contacting us!', 'success')
        session['message_sent'] = True
        return redirect(url_for('home.contact'))
    
    message_sent = session.pop('message_sent', False)
    return render_template('contact.html', message_sent=message_sent)
    
# Helper function to get election results
def get_election_results(election_id):
    results = db.session.query(
        Candidate.name, db.func.count(Vote.id).label('votes')
    ).join(Vote).filter(Vote.election_id == election_id).group_by(Candidate.name).all()
    return results
