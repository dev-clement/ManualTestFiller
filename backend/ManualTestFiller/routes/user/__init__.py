from flask import Blueprint

user_bp = Blueprint('user', __name__, url_prefix='/user')

# Import routes so they're registered when blueprint is imported
from . import register, signin, logout