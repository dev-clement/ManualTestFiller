from flask import jsonify, request
from ManualTestFiller.models import User
from werkzeug.security import generate_password_hash
from ManualTestFiller import db
from .base_user_view import BaseUserView

class UserRegisterView(BaseUserView):
    def post(self):
        """Method used to register a new user to the database"""
        required_fields = ['email', 'password']
        data, error, status = self.validate_request(required_fields=required_fields)
        if error:
            return error, status
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'status': 'error'
                            , 'message': 'Email and / or password isn\'t present'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'status': 'error'
                            ,'message': 'Email already exists'}), 409
        
        user = User(email=email, password=generate_password_hash(password))
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error'
                            , 'message': f'Database error, details: {str(e)}'}), 500

        return jsonify({'status': 'success'
                        , 'message': 'User registered successfully'}), 201

