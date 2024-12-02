from models.schemas.customerAccountSchema import customer_accounts_schema
from services import customerAccountService
from flask import request, jsonify

def find_all():
    customer_accounts = customerAccountService.find_all()
    return customer_accounts_schema.jsonify(customer_accounts), 200

def login_customer():
    customer = request.json
    user = customerAccountService.login_customer(customer['username'], customer['password'])
    if user:
        return jsonify(user), 200
    else:
        resp={
            "message":"failure"
        }
        return jsonify(resp), 400