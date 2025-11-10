from flask import jsonify, request
from ManualTestFiller.models import User
from werkzeug.security import generate_password_hash
from ManualTestFiller import db
from . import user_bp

# ----------------------------------------
# Register route
# ----------------------------------------
@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required for authentication !'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400

    user = User(email=email, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User register successfully'}), 201