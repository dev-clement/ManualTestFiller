from flask.views import MethodView
from flask import request, jsonify

class BaseUserView(MethodView):
    def validate_request(self, required_fields):
        data = request.get_json()
        for field in required_fields:
            if field not in data:
                return None, jsonify({'error': f'{field} is required'}), 400
            return data, None, None
