from flask import Blueprint, request, jsonify, session
from werkzeug import generate_password_hash, check_password_hash
from ManualTestFiller.models import User
from ManualTestFiller import db

user_bp = Blueprint('user', __name__, url_prefix='/user')

# ----------------------------------------
# Register route
# ----------------------------------------
@user_bp('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required for authentication !'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'error', 'Email already exists'}), 400

    user = User(email=email, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()

    return jsonify({'message', 'User has been authenticated successfully'}), 201

# ----------------------------------------
# Sign in route
# ----------------------------------------
@user_bp('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error', 'Invalid credential, no such user exist'}), 401
    
    session['user_id'] = user.id
    return jsonify({'message', 'Signed in successfully'})

# ----------------------------------------
# Sign out route
# ----------------------------------------
@user_bp('/signout', methods=['POST'])
def signout():
    session.pop('user_id', None)
    return jsonify({'message', 'Signed out successfully'}), 200
