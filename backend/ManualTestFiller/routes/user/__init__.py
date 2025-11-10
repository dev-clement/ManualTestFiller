from flask import Blueprint

user_bp = Blueprint('user', __name__, url_prefix='/user')

# Import routes so they're registered when blueprint is imported
def register_user_routes():
    from .register import UserRegisterView

    user_bp.add_url_rule(
        '/register'
        , view_func=UserRegisterView.as_view('register')
        , methods=['POST']
    )