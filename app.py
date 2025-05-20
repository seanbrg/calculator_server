from flask import Flask, request
from calculator.operations import perform_operation
from calculator.stack import StackManager
from calculator.history import HistoryManager
from calculator.utils import response

app = Flask(__name__)

# Global memory-only objects
stack = StackManager()
history = HistoryManager()

# -------- Health Endpoint --------
@app.route('/calculator/health', methods=['GET'])
def health():
    return response("OK")

# -------- Independent Calculation --------
@app.route('/calculator/independent/calculate', methods=['POST'])
def independent_calculate():
    data = request.get_json()
    args = data.get('arguments', [])
    operation = data.get('operation', '').lower()

    try:
        result = perform_operation(operation, args)
        history.record('INDEPENDENT', operation, args, result)
        return response(result=result)
    except ValueError as ve:
        return response(error_message=str(ve), status=409)

# -------- Stack: Get Size --------
@app.route('/calculator/stack/size', methods=['GET'])
def stack_size():
    return response(result=stack.size())

# -------- Stack: Add Arguments --------
@app.route('/calculator/stack/arguments', methods=['PUT'])
def stack_push():
    data = request.get_json()
    args = data.get('arguments', [])
    stack.push(args)
    return response(result=stack.size())

# -------- Stack: Perform Operation --------
@app.route('/calculator/stack/operate', methods=['GET'])
def stack_operate():
    operation = request.args.get('operation', '').lower()
    try:
        args = stack.peek(operation)
        result = perform_operation(operation, args)
        stack.pop(len(args))  # Only pop after successful execution
        history.record('STACK', operation, args, result)
        return response(result=result)
    except ValueError as ve:
        return response(error_message=str(ve), status=409)

# -------- Stack: Remove Arguments --------
@app.route('/calculator/stack/arguments', methods=['DELETE'])
def stack_remove():
    try:
        count = int(request.args.get('count', 0))
    except ValueError:
        msg = str('Invalid count parameter')
        return response(error_message=msg, status=409)

    if stack.size() < count:
        msg = str(f"Error: cannot remove {count} from the stack. It has only {stack.size()} arguments")
        return response(error_message=msg, status=409)

    stack.pop(count)
    return response(result=stack.size())

# -------- Fetch History --------
@app.route('/calculator/history', methods=['GET'])
def get_history():
    flavor = request.args.get('flavor', None)
    try:
        entries = history.get(flavor)
        return response(result=entries)
    except ValueError as ve:
        return response(error_message=str(ve), status=409)