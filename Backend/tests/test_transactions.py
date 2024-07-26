from Backend.tests.conftest import test_client, init_database, get_jwt_token
import json


def test_add_transaction(test_client, init_database):

    jwt_token = get_jwt_token(test_client)

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


def test_view_transactions(test_client):

    jwt_token = get_jwt_token(test_client)

    headers = {'Authorization': f'Bearer {jwt_token}'}
    response = test_client.get('/transactions', headers=headers)

    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)


def test_get_portfolio_value(test_client):

    jwt_token = get_jwt_token(test_client)

    headers = {'Authorization': f'Bearer {jwt_token}'}
    response = test_client.get('/portfolio', headers=headers)

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'total_value' in data


def test_update_transaction(test_client, init_database):

    jwt_token = get_jwt_token(test_client)

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

    response_json = json.loads(response.data)
    transaction_id = response_json.get('id')

    response = test_client.put(f'/transactions/update/{transaction_id}',
                               data=json.dumps({
                                   'amount': 0.75
                               }),
                               headers=headers,
                               content_type='application/json')


def test_delete_transaction(test_client, init_database):

    jwt_token = get_jwt_token(test_client)

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

    response_json = json.loads(response.data)
    transaction_id = response_json.get('id')


def test_get_historical_data(test_client, init_database):

    jwt_token = get_jwt_token(test_client)

    headers = {'Authorization': f'Bearer {jwt_token}'}
    response = test_client.get('/transactions/history',
                               headers=headers,
                               query_string={'user_id': 1, 'start_date': '2024-01-01', 'end_date': '2024-12-31'})

    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)


def test_register_user(test_client, init_database):

    response = test_client.post('/register',
                                data=json.dumps({
                                    'username': 'test1user',
                                    'password': 'password'
                                }),
                                content_type='application/json')

    assert response.status_code == 201


def test_login_user(test_client, init_database):

    test_client.post('/register',
                     data=json.dumps({
                         'username': 'testuser',
                         'password': 'password'
                     }),
                     content_type='application/json')

    response = test_client.post('/login',
                                data=json.dumps({
                                    'username': 'testuser',
                                    'password': 'password'
                                }),
                                content_type='application/json')

    assert response.status_code == 200


CRYPTOCURRENCIES = ["bitcoin", "ethereum", "litecoin", "ripple", "dogecoin", "cardano", "polkadot", "solana", "chainlink", "uniswap"]


def test_get_prices(test_client, init_databased):

    jwt_token = get_jwt_token(test_client)

    headers = {
        'Authorization': f'Bearer {jwt_token}'

    }
    response = test_client.get('/prices', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'prices' in data
    assert 'message' in data
    assert data['message'] == 'Current prices of top 10 cryptocurrencies in USD'
    assert isinstance(data['prices'], dict)
    for crypto in CRYPTOCURRENCIES:
        assert crypto in data['prices']
