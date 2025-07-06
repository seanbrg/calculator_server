import os, time, logging
from flask import Flask, request, g
from calculator.operations import perform_operation
from calculator.stack import StackManager
from calculator.history import HistoryManager
from calculator.utils import response, setup_logger

# -------- Initialize loggers --------
LOG_DIR = 'logs'
os.makedirs(LOG_DIR, exist_ok=True)
# --- Initialize loggers ---
# request-logger logs incoming requests and durations to requests.log + stdout
request_logger = setup_logger('request-logger', LOG_DIR, logging.INFO, 'requests.log', to_stdout=True)
# stack-logger logs stack operations to stack.log
stack_logger = setup_logger('stack-logger', LOG_DIR, logging.INFO, 'stack.log')
# independent-logger logs independent calculations to independent.log
independent_logger = setup_logger('independent-logger', LOG_DIR, logging.DEBUG, 'independent.log')

# -------- Global variables --------
app = Flask(__name__)
request_counter = 1
stack = StackManager()
history = HistoryManager()

# -------- Request logging --------
@app.before_request
def log_request_start():
    """
    Log incoming request details before processing and assign a request number.
    """
    global request_counter
    g.start_time = time.time()
    g.request_number = request_counter
    request_logger.info(
        f"Incoming request | #{g.request_number} | resource: {request.path} | HTTP Verb {request.method} | request #{g.request_number}"
    )
    request_counter += 1

@app.after_request
def log_request_end(response):
    """
    Log request processing duration at DEBUG level.
    """
    duration_ms = int((time.time() - g.start_time) * 1000)
    # DEBUG: request duration
    request_logger.debug(
        f"request #{g.request_number} duration: {duration_ms}ms | request #{g.request_number}"
    )
    return response

# -------- Error handler --------
@app.errorhandler(Exception)
def handle_error(e):
    # skip logging for 400 Bad Request errors
    if hasattr(e, 'code') and e.code == 400:
        return response(error_message=str(e), status=400)
    msg = str(e)
    request_logger.error(
        f"Server encountered an error ! message: {msg} | request #{g.request_number}"
    )
    return response(error_message=str(e), status=500)


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

        independent_logger.info(
            f"Performing operation {operation}. Result is {result} | request #{g.request_number}"
        )
        independent_logger.debug(
            f"Performing operation: {operation}({','.join(map(str,args))}) = {result} | request #{g.request_number}"
        )

        return response(result=result)
    except ValueError as ve:
        return response(error_message=str(ve), status=400)

# -------- Stack: Get Size --------
@app.route('/calculator/stack/size', methods=['GET'])
def stack_size():
    size = stack.size()
    # INFO: stack size
    stack_logger.info(
        f"Stack size is {size} | request #{g.request_number}"
    )
    # DEBUG: show full content (first element is top)
    content = list(reversed(stack._items))
    stack_logger.debug(
        f"Stack content (first == top): {content} | request #{g.request_number}"
    )
    return response(result=size)

# -------- Stack: Add Arguments --------
@app.route('/calculator/stack/arguments', methods=['PUT'])
def stack_push():
    data = request.get_json() or {}
    args = data.get('arguments', [])
    before = stack.size()
    stack.push(args)
    after = stack.size()
    history.record('STACK', 'push', args, after)
    # INFO then DEBUG
    stack_logger.info(
        f"Adding total of {len(args)} argument(s) to the stack | Stack size: {after} | request #{g.request_number}"
    )
    stack_logger.debug(
        f"Adding arguments: {args} | Stack size before {before} | stack size after {after} | request #{g.request_number}"
    )
    return response(result=after)

# -------- Stack: Perform Operation --------
@app.route('/calculator/stack/operate', methods=['GET'])
def stack_operate():
    data = request.get_json()
    operation = data.get('operation', '').lower()
    try:
        args = stack.peek(operation)
        result = perform_operation(operation, args)
        stack.pop(len(args))  # Only pop after successful execution
        history.record('STACK', operation, args, result)
        after_size = stack.size()
        # INFO then DEBUG
        stack_logger.info(
            f"Performing operation {operation}. Result is {result} | stack size: {after_size} | request #{g.request_number}"
        )
        stack_logger.debug(
            f"Performing operation: {operation}({','.join(map(str, args))}) = {result} | request #{g.request_number}"
        )
        return response(result=result)
    except ValueError as ve:
        return response(error_message=str(ve), status=400)

# -------- Stack: Remove Arguments --------
@app.route('/calculator/stack/arguments', methods=['DELETE'])
def stack_remove():
    try:
        count = int(request.args.get('count', 0))
    except ValueError:
        msg = str('Invalid count parameter')
        return response(error_message=msg, status=400)

    if stack.size() < count:
        msg = str(f"Error: cannot remove {count} from the stack. It has only {stack.size()} arguments")
        return response(error_message=msg, status=400)

    before = stack.size()
    stack.pop(count)
    after = stack.size()
    history.record('STACK', 'pop', count, after)
    stack_logger.info(
        f"Removing total {count} argument(s) from the stack | Stack size: {after} | request #{g.request_number}"
    )
    return response(result=stack.size())

# -------- Fetch History --------
@app.route('/calculator/history', methods=['GET'])
def get_history():
    flavor = request.args.get('flavor', None)
    try:
        entries = history.get(flavor)
        if flavor == 'independent':
            independent_logger.info(
            f"History: So far total {len(entries)} independent actions | request #{g.request_number}"
            )
        else:
            stack_logger.info(
            f"History: So far total {len(entries)} stack actions | request #{g.request_number}"
            )
        return response(result=entries)
    except ValueError as ve:
        return response(error_message=str(ve), status=400)

# -------- Logger Level Endpoints --------
@app.route('/logs/level', methods=['GET'])
def get_log_level():
    name = request.args.get('logger-name')
    if not name:
        return 'Missing logger-name', 409
    logger = logging.getLogger(name)
    if not logger.handlers:
        return f'Logger "{name}" not found', 409
    level = logging.getLevelName(logger.level)
    # Return plain text level
    return level, 200

@app.route('/logs/level', methods=['PUT'])
def set_log_level():
    name = request.args.get('logger-name')
    lvl = request.args.get('logger-level')
    if not name:
        return 'Missing logger-name', 409
    if lvl not in ('ERROR', 'INFO', 'DEBUG'):
        return 'Invalid logger-level', 409
    logger = logging.getLogger(name)
    if not logger.handlers:
        return f'Logger "{name}" not found', 409
    logger.setLevel(getattr(logging, lvl))
    # Return new level as plain text
    return lvl, 200


# -------- Run App --------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8496)