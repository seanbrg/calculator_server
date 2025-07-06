Calculator HTTP API Microservice

Description:
A Dockerized Python Flask service providing a REST-style HTTP API for basic arithmetic operations (add, subtract, multiply, divide) and in-memory history retrieval.

Prerequisites:

* Docker Engine v20+
* (Optional) Python 3.8+ and pip

Installation:

1. Clone repository:
   git clone https://github.com/seanbrg/calculator_server
   cd calculator-server
2. Build Docker image:
   docker build --platform linux/amd64 -t calculator-server .

Configuration (optional):

* PORT (default: 4785)
* LOG\_LEVEL (INFO, DEBUG, etc.)

Running:
With Docker:
docker run -d -p 4785:4785 --name calculator-server calculator-server

Without Docker:
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py

Endpoints (can be easily accessed via Postman):

1. Health check:
   GET /calculator/health
   Response: {"status":"ok","uptime":"HH\:MM\:SS"}

2. Arithmetic operations:
   GET /calculator/{operation}?a=<number>\&b=<number>
   {operation}: add, subtract, multiply, divide
   Example: curl "[http://localhost:4785/calculator/add?a=4\&b=5](http://localhost:4785/calculator/add?a=4&b=5)"
   Response: {"request\_id"\:n,"operation":"add","operands":\[4,5],"result":9}

3. History retrieval:
   GET /calculator/history
   Response: List of past requests with ID, operation, operands, and result.

Logging:

* Format: DD-MM-YYYY HH\:MM\:SS.mmm LEVEL: message | request #n
* Levels: INFO, DEBUG, ERROR

Testing:

* Manual testing can be done via curl or Postman

Contributing:

* Fork the repo
* Create branch: git checkout -b feature/YourFeature
* Commit and push changes
* Open a pull request

License:
MIT
