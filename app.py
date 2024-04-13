from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from features.models import db  # Import db from models.py

# db = SQLAlchemy()




def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.template_folder = 'features/templates'
    app.static_folder = 'features/static'
    app.secret_key = 'your_secret_key_here'

    db.init_app(app)

    from features.signup import signup_routes
    from features.login import login_routes
    from features.main import main_routes
    # from features.routes import main_routes

    app.register_blueprint(main_routes, name='main_routes')
    app.register_blueprint(signup_routes)
    app.register_blueprint(login_routes)
    # app.register_blueprint(main_routes)


    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
