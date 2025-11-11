from flask import request, jsonify, session
from werkzeug.security import check_password_hash
from ManualTestFiller.models import User
from . import user_bp

# ----------------------------------------
# Sign in route
# ----------------------------------------
@user_bp.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid credential, no such user exist'}), 401
    
    session['user_id'] = user.id
    return jsonify({'message': 'Signed in successfully'})