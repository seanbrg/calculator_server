Flask Calculator Server
=======================

Overview
--------
This project implements a simple Flask-based calculator server that supports both:
1. Independent calculations (client provides arguments and operation directly)
2. Stack-based operations (arguments are pushed to a stack and consumed when operations are performed)

The server supports basic arithmetic operations like addition, subtraction, multiplication, division, exponentiation, absolute value, and factorial. It also keeps a history of all successful operations performed, which can be queried through a dedicated endpoint.

API endpoints are available under the `/calculator/` route.

System Requirements
-------------------
- Python 3.8 or higher
- Flask 2.0 or higher

Installation
------------
1. Clone the project to your machine.
2. Create a virtual environment (optional but recommended):
   python -m venv venv
   venv\Scripts\activate    (Windows)
   source venv/bin/activate (Linux/macOS)
3. Install dependencies:
   pip install -r requirements.txt

Running the Server
------------------
Use the provided `run.bat` file to start the server on port 8496:

    run.bat

This will set the necessary environment variables and run the app using Flask's built-in development server.

Usage
-----
- Visit http://localhost:8496/calculator/health to confirm the server is running.
- Use tools like Postman or `curl` to interact with the API.
- All responses (except /health) return JSON with a `result` or `errorMessage`.

Structure
---------
- `app.py` — main server logic and route handling
- `calculator/operations.py` — core math logic
- `calculator/stack.py` — stack logic for arguments
- `calculator/history.py` — logs and retrieves past operations
- `calculator/utils.py` — helper functions for formatting responses and history entries
- `requirements.txt` — dependency list
- `run.bat` — script to launch the server with environment setup

License
-------
This project is for educational use only.

Author
------
Sean Berger
