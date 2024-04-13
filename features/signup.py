from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from .models import AccountInfo

from features.models import db, AccountInfo



signup_routes = Blueprint('signup', __name__)

@signup_routes.route('/signup')
def signup():
    return render_template("signup.html")

@signup_routes.route('/form_signup', methods=['POST'])
def signup_submit():
    # from .models import AccountInfo 

    error_message = None
    user_name = request.form['name']
    user_surname = request.form['surname']
    github_username = request.form['github_username']
    user_email = request.form['email']
    access_key = request.form['access_key']
    secrete_access_key = request.form['secrete_accesskey']
    user_password = request.form['password']
    user_confirm_password = request.form['confirm_password']

    if user_password != user_confirm_password:
        error_message = "Password and Confirm Password do not match"
    else:
        existing_user = AccountInfo.query.filter_by(email=user_email).first()
        if existing_user:
            error_message = "User already exists"
        else:
            new_user = AccountInfo(name=user_name, email=user_email, password=user_password, surname = user_surname, githubusername = github_username, accesskey = access_key, secreteaccesskey = secrete_access_key)    #confirm_password=user_confirm_password
            try:
                db.session.add(new_user)
                db.session.commit()
                print("User added successfully:", new_user.name)
                tasks = AccountInfo.query.all()
                return render_template("login.html", tasks=tasks)
            except Exception as e:
                db.session.rollback()
                print("Error adding user:", str(e))

    return render_template("signup.html", error_message=error_message)
