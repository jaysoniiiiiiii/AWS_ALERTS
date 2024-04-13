from flask import Blueprint, render_template
from .models import AccountInfo

# Create a Blueprint object for your routes
main_routes = Blueprint('main', __name__)

# Define your routes using the `route` decorator
@main_routes.route('/')
def index():
    # Example: Querying a model and passing data to a template
    data = AccountInfo.query.all()
    return render_template('index.html', data=data)
