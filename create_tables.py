from features.models import db
from app import create_app

def main():
    # Create the Flask app
    app = create_app()

    # Establish the application context
    with app.app_context():
        # Now you can use db within the application context
        db.create_all()

if __name__ == "__main__":
    main()
