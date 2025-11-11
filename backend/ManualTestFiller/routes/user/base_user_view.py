from flask.views import MethodView
from flask import request, jsonify
from ManualTestFiller.models.user import User
from werkzeug.security import check_password_hash

class BaseUserView(MethodView):
    def validate_request(self, required_fields):
        data = request.get_json()
        for field in required_fields:
            if field not in data:
                return None, jsonify({'error': f'{field} is required'}), 400
        return data, None, None
    
    def get_user_by_email(self, email):
        """Check if there is a user in the database with the email specified"""
        return User.query.filter_by(email=email).first()
    
    def verify_password(self, stored_hash, provided_password):
        """Check if the given password is correct in the database"""
        return check_password_hash(stored_hash, provided_password)
    
    def respond(self, message, status_code=200):
        """Utility to make a consistent JSON response"""
        return jsonify({'message': message, 'status_code': status_code}), status_code
