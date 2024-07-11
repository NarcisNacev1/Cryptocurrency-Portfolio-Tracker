# test_transactions.py

import json
from Backend.tests.conftest import test_client, init_database, get_jwt_token

# Test for adding a transaction with specific ID
def test_add_transaction(test_client, init_database):
    # Obtain JWT token
    jwt_token = get_jwt_token(test_client)

    # Make a POST request with authentication header
    headers = {'Authorization': f'Bearer {jwt_token}'}
    response = test_client.post('/transactions',
                                data=json.dumps({
                                    'user_id': 1,
                                    'cryptocurrency': 'bitcoin',
                                    'amount': 0.5,
                                    'transaction_type': 'buy',
                                    'transaction_price': 45000
                                }),
                                headers=headers,
                                content_type='application/json')

    assert response.status_code == 201
    assert b'Transaction was made successfully' in response.data


# Test for viewing transactions
def test_view_transactions(test_client):
    # Obtain JWT token
    jwt_token = get_jwt_token(test_client)

    # Make a GET request with authentication header
    headers = {'Authorization': f'Bearer {jwt_token}'}
    response = test_client.get('/transactions', headers=headers)

    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)


# Test for getting portfolio value
def test_get_portfolio_value(test_client):
    # Obtain JWT token
    jwt_token = get_jwt_token(test_client)

    # Make a GET request with authentication header
    headers = {'Authorization': f'Bearer {jwt_token}'}
    response = test_client.get('/portfolio', headers=headers)

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'total_value' in data


# Test for updating a transaction
import json

import json

def test_update_transaction(test_client, init_database):
    # Obtain JWT token
    jwt_token = get_jwt_token(test_client)

    # Make a POST request to add a transaction first
    headers = {'Authorization': f'Bearer {jwt_token}'}
    response = test_client.post('/transactions',
                                data=json.dumps({
                                    'user_id': 1,
                                    'cryptocurrency': 'bitcoin',
                                    'amount': 0.5,
                                    'transaction_type': 'buy',
                                    'transaction_price': 45000
                                }),
                                headers=headers,
                                content_type='application/json')

    assert response.status_code == 201

    # Get transaction ID from response
    response_json = json.loads(response.data)
    transaction_id = response_json.get('id')  # Use .get() to safely get id or None


    # Make a PUT request to update the transaction
    response = test_client.put(f'/transactions/update/{transaction_id}',
                               data=json.dumps({
                                   'amount': 0.75
                               }),
                               headers=headers,
                               content_type='application/json')





def test_delete_transaction(test_client, init_database):
    # Obtain JWT token
    jwt_token = get_jwt_token(test_client)

    # Make a POST request to add a transaction first
    headers = {'Authorization': f'Bearer {jwt_token}'}
    response = test_client.post('/transactions',
                                data=json.dumps({
                                    'user_id': 1,
                                    'cryptocurrency': 'bitcoin',
                                    'amount': 0.5,
                                    'transaction_type': 'buy',
                                    'transaction_price': 45000
                                }),
                                headers=headers,
                                content_type='application/json')

    assert response.status_code == 201  # Check if transaction creation was successful

    # Extract transaction ID from the response
    response_json = json.loads(response.data)
    transaction_id = response_json.get('id')



def test_get_historical_data(test_client, init_database):
    # Obtain JWT token
    jwt_token = get_jwt_token(test_client)

    # Make a GET request with authentication header
    headers = {'Authorization': f'Bearer {jwt_token}'}
    response = test_client.get('/transactions/history',
                               headers=headers,
                               query_string={'user_id': 1, 'start_date': '2024-01-01', 'end_date': '2024-12-31'})

    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)


# Test for registering a new user

def test_register_user(test_client, init_database):
    # Make a POST request to register a new user
    response = test_client.post('/register',
                                data=json.dumps({
                                    'username': 'test1user',
                                    'password': 'password'
                                }),
                                content_type='application/json')

    assert response.status_code == 201  # Expected status

def test_login_user(test_client, init_database):
    # First, register a new user
    test_client.post('/register',
                     data=json.dumps({
                         'username': 'testuser',
                         'password': 'password'
                     }),
                     content_type='application/json')

    # Make a POST request to login with the registered user
    response = test_client.post('/login',
                                data=json.dumps({
                                    'username': 'testuser',
                                    'password': 'password'
                                }),
                                content_type='application/json')

    assert response.status_code == 200  # Expected status code for successful login