from flask import session, jsonify
from .base_user_view import BaseUserView

class SignOutView(BaseUserView):
    def post(self):
        """Sign out method"""
        session.pop('user_id', None)
        return jsonify({'message': 'Signed out successfully'}), 200

def register_signout_route(user_bp):
    """Registering the sign out route"""
    user_bp.add_url_rule('/signout', view_func=SignOutView.as_view('signout'))
