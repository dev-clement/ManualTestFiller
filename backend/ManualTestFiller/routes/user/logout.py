from flask import session, jsonify
from . import user_bp

# ----------------------------------------
# Sign out route
# ----------------------------------------
@user_bp.route('/signout', methods=['POST'])
def signout():
    session.pop('user_id', None)
    return jsonify({'message': 'Signed out successfully'}), 200