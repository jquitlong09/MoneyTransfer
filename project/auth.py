from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Audit
from . import db
from flask_login import login_user, login_required, logout_user
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
@cross_origin()
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    print(email, password)

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        return 'Please check your login details and try again.', 401
    login_user(user, remember=remember)

    # Add audit
    audit = Audit(action="User login", user_id=user.id)
    db.session.add(audit)
    db.session.commit()

    access_token = create_access_token(identity=email)
    response = {"access_token":access_token}
    return response, 200

@auth.route('/signup', methods=['POST'])
def signup():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    
    # validate required input
    if email is None or name is None or password is None:
        return 'Fill up required fields'

    # if this returns a user, then the email already exists in database
    user = User.query.filter_by(email=email).first()

    if user: 
        return 'Duplicate'

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return 'Signup'

@auth.route('/logout', methods=['POST'])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    logout_user()
    return response
