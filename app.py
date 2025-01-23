from flask import Flask 
from flask_migrate import Migrate 
from extensions import db 
from routes import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voting.db'
    app.config['SECRET_KEY'] = 'd5s6f4ad56sf456sadf45sda1vg48bdfgb'

   # Initialize extensions 
    db.init_app(app) 
    migrate = Migrate(app, db)

    # Register blueprints
    register_blueprints(app)  # Correct function call

    # Create database tables
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=8000)
