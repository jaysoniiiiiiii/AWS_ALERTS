from flask import Blueprint, render_template, request, redirect, url_for, session
from app import db
from .models import AccountInfo

from features.models import db, AccountInfo



login_routes = Blueprint('login', __name__)

@login_routes.route('/')
def login():
    return render_template("login.html")

@login_routes.route('/form_login', methods=['POST'])
def login_submit():
    if request.method == 'POST':
        error_message = None
        # user_name = request.form['name']
        user_email = request.form['email']
        user_password = request.form['password']



        user = AccountInfo.query.filter_by(email=user_email, password=user_password).first()

        if user:
            # Login successful, redirect to a dashboard or profile page
            # return render_template('main.html',  tasks=tasks)
            session['user_id'] = user.id
            return redirect(url_for('main_routes.main_page'))
        else:
            # Login failed, show an error message
            error_message = "Invalid email or password. Please try again."
            return render_template("login.html", error_message=error_message)
    else:
        return render_template("login.html")