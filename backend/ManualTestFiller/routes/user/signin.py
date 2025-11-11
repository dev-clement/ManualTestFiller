from flask import request, jsonify, session
from werkzeug.security import check_password_hash
from ManualTestFiller.models import User
from .base_user_view import BaseUserView

class SignInView(BaseUserView):
    def post(self):
        """Method used in order to sign an user in"""
        data, error, status = self.validate_request(['email', 'password'])
        if error:
            return error, status
        email = data['email']
        password = data['password']
        user = self.get_user_by_email(email=email)
        
        if not user:
            return jsonify({'error': 'Invalid email or password !'}), 401

        if not self.verify_password(user.password, password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Here in case of you making a JWT, it will written out there
        session['user_id'] = user.id
        return self.respond(f'Welcome back, {email}')

def register_signin_route(user_bp):
    """Register all signin route from the flask blueprint"""
    user_bp.add_url_rule('/signin', view_func=SignInView.as_view('signin'))
