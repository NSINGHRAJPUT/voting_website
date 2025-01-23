from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models import Election, Vote, User
from extensions import db
from flask_login import login_required, current_user

voting_bp = Blueprint('voting', __name__)

@voting_bp.route('/elections')
@login_required
def elections():
    elections = Election.query.filter_by(status='Ongoing').all()
    return render_template('elections.html', elections=elections)

@voting_bp.route('/election/<int:election_id>/vote', methods=['GET', 'POST'])
@login_required
def vote(election_id):
    election = Election.query.get_or_404(election_id)

    if election.status != 'Ongoing':
        flash("This election is not open for voting.", "error")
        return redirect(url_for('voting.elections'))

    # Check if the user has already voted in this election
    existing_vote = Vote.query.filter_by(election_id=election_id, user_id=current_user.id).first()
    if existing_vote:
        flash("You have already voted in this election.", "error")
        return redirect(url_for('voting.elections'))

    if request.method == 'POST':
        candidate_id = request.form.get('candidate_id')
        if not candidate_id:
            flash("Please select a candidate.", "error")
            return redirect(url_for('voting.vote', election_id=election_id))
        
        new_vote = Vote(title=f"Vote in Election {election_id}", user_id=current_user.id, election_id=election_id)
        db.session.add(new_vote)
        db.session.commit()
        flash("Your vote has been recorded. Thank you for voting!", "success")
        return redirect(url_for('voting.elections'))
    
    candidates = election.candidates  # Assuming you have a candidates relationship in the Election model
    return render_template('vote.html', election=election, candidates=candidates)

@voting_bp.route('/results/<int:election_id>')
@login_required
def results(election_id):
    election = Election.query.get_or_404(election_id)
    if election.status != 'Ended':
        flash("The results for this election are not available yet.", "error")
        return redirect(url_for('voting.elections'))

    # Get results
    results = db.session.query(Vote.candidate_id, db.func.count(Vote.id).label('vote_count')) \
                        .filter(Vote.election_id == election_id) \
                        .group_by(Vote.candidate_id) \
                        .all()
    
    return render_template('results.html', election=election, results=results)
