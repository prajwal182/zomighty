# app/errors.py
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    return jsonify(payload), status_code

def register_error_handlers(app):
    
    # 400: Bad Request (e.g. Malformed JSON)
    @app.errorhandler(400)
    def bad_request(error):
        return error_response(400, message="Bad Request: Check your JSON or parameters")

    # 404: Not Found (e.g. Wrong URL)
    @app.errorhandler(404)
    def not_found_error(error):
        return error_response(404, message="Resource not found")

    # 405: Method Not Allowed (e.g. POST to a GET route)
    @app.errorhandler(405)
    def method_not_allowed(error):
        return error_response(405, message="Method not allowed for this endpoint")

    # 500: Internal Server Error (e.g. Your code crashed)
    @app.errorhandler(500)
    def internal_error(error):
        # In a real app, we would log the specific error to a file here
        return error_response(500, message="An internal error occurred")