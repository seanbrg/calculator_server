from flask import jsonify

def response(result=None, error_message=None, status=200):
    """
    Standardized JSON response for success or error.

    - Only field is either 'result' or 'errorMessage', not both.
    - Status defaults to 200 for success, override with 409 for errors.
    """
    if error_message is not None:
        return jsonify({'errorMessage': error_message}), status
    else:
        return jsonify({'result': result}), status
