from flask import jsonify
from service.models import DataValidationError
from service import app
from service.common import status

@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """Handle Data Validation Error"""
    message = str(error)
    app.logger.error(message)
    return jsonify(status=status.HTTP_400_BAD_REQUEST, error="Bad Request", message=message), status.HTTP_400_BAD_REQUEST

@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(error):
    """Handle 404 Not Found"""
    message = str(error)
    app.logger.error(message)
    return jsonify(status=status.HTTP_404_NOT_FOUND, error="Not Found", message=message), status.HTTP_404_NOT_FOUND
