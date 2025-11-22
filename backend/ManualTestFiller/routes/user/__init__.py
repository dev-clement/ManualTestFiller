from flask import Blueprint

# Import routes so they're registered when blueprint is imported
def create_user_blueprint():
    user_bp = Blueprint('user', __name__, url_prefix='/user')

    from .register import register_register_route
    from .signin import register_signin_route
    from .signout import register_signout_route
    register_register_route(user_bp=user_bp)
    register_signin_route(user_bp=user_bp)
    register_signout_route(user_bp=user_bp)
    return user_bp

