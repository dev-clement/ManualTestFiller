from flask import Blueprint

# Import routes so they're registered when blueprint is imported
def create_user_blueprint():
    user_bp = Blueprint('user', __name__, url_prefix='/user')

    from .register import register_user_route
    register_user_route(user_bp=user_bp)
    return user_bp

