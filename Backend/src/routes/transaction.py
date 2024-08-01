from flask import Blueprint, request, jsonify, session
from Backend.src.models import Transaction
from Backend.src.extensions import db
from flask_jwt_extended import jwt_required
from Backend.src.models import PortfolioHistory
from Backend.src.services.crypto import get_crypto_prices
from Backend.src.services.crypto import get_cryptos
from flask_jwt_extended import get_jwt_identity
from Backend.src.models import User
import logging

transaction_routes = Blueprint('transactions', __name__)
logger = logging.getLogger(__name__)

CRYPTOCURRENCIES = [
    "bitcoin",
    "ethereum",
    "litecoin",
    "ripple",
    "dogecoin",
    "cardano",
    "polkadot",
    "solana",
    "chainlink",
    "uniswap",
    "binancecoin",
    "stellar",
    "vechain",
    "tron",
    "monero",
    "dash",
    "tezos",
    "aave",
    "cosmos",
    "avalanche-3"
]


@transaction_routes.route('/prices', methods=['GET'])
@jwt_required()
def view_prices():
   try:
       prices = get_cryptos(CRYPTOCURRENCIES)
       response = {
           "message": 'Current prices of top 10 cryptocurrencies in USD',
           "price": prices
       }
       return jsonify(response), 200
   except Exception as e:
       return jsonify({'error:': str(e)}), 500


@transaction_routes.route('/price/<string:crypto>', methods=['GET'])
@jwt_required()
def view_price(crypto):
    try:
        price = get_crypto_prices(crypto)
        response = {
            "message": f"The current price of {crypto} in USD is : ",
            "prices": f'{price} USD'
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@transaction_routes.route('/transactions', methods=["POST"])
@jwt_required()
def add_transaction():
    current_user = get_jwt_identity()
    current_username = current_user['username']

    user = User.query.filter_by(username=current_username).first()
    if not user:
        return jsonify({'msg': 'User not found'}), 404

    user_id = user.id
    request_user_id = request.json.get('user_id')

    if request_user_id != user_id:
        return jsonify({'msg': 'Unauthorized'}), 403

    try:
        data = request.get_json()
        session['last_transaction'] = data
        logger.debug("Session data set: %s", session['last_transaction'])
        crypto_price = get_crypto_prices(data['cryptocurrency'])

        transaction = Transaction(
            user_id=data['user_id'],
            cryptocurrency=data['cryptocurrency'],
            amount=data['amount'],
            transaction_type=data['transaction_type'],
            transaction_price=crypto_price
        )
        db.session.add(transaction)
        db.session.commit()
        return jsonify({'msg': 'Transaction was made successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@transaction_routes.route('/transactions', methods=["GET"])
@jwt_required()
def view_transactions():
    transactions = Transaction.query.all()
    return jsonify([transaction.as_dict() for transaction in transactions])


@transaction_routes.route('/transactions/update/<int:id>', methods=["PUT"])
@jwt_required()
def update_transaction(id):
    try:
        current_user = get_jwt_identity()
        current_username = current_user['username']

        user = User.query.filter_by(username=current_username).first()
        if not user:
            return jsonify({'msg': 'User not found'}), 404

        user_id = user.id
        request_user_id = request.json.get('user_id')

        if request_user_id != user_id:
            return jsonify({'msg': 'Unauthorized'}), 403

        data = request.get_json()
        transaction = Transaction.query.get_or_404(id)
        transaction.amount = data.get('amount', transaction.amount)
        transaction.transaction_price = data.get('transaction_price', transaction.transaction_price)
        db.session.commit()
        return jsonify({'message': 'Transaction updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@transaction_routes.route('/transactions/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_transaction(id):
    try:
        transaction = Transaction.query.get_or_404(id)
        db.session.delete(transaction)
        db.session.commit()
        return jsonify({'message': 'Transaction deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@transaction_routes.route('/transactions/delete/all', methods=['DELETE'])
@jwt_required()
def delete_all_transactions():
    try:
        transactions = Transaction.query.all()
        for transaction in transactions:
            db.session.delete(transaction)
        db.session.commit()
        return jsonify({'message': 'Transactions deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@transaction_routes.route('/session_data', methods=['GET'])
@jwt_required()
def view_session():
    session_data = dict(session)
    return jsonify(session_data), 200


@transaction_routes.route('/transactions/history', methods=['GET'])
@jwt_required()
def get_historical_data():
    try:
        current_user = get_jwt_identity()
        username = current_user['username']

        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        user_id = user.id
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        query = Transaction.query.filter(Transaction.user_id == user_id)
        if start_date:
            query = query.filter(Transaction.transaction_date >= start_date)
        if end_date:
            query = query.filter(Transaction.transaction_date <= end_date)

        transactions = query.all()

        total_value = 0
        total_gain_loss = 0
        crypto_holdings = {}

        for transaction in transactions:
            crypto = transaction.cryptocurrency
            if crypto not in crypto_holdings:
                crypto_holdings[crypto] = 0

            if transaction.transaction_type == 'buy':
                crypto_holdings[crypto] += transaction.amount
                total_value += transaction.amount * transaction.transaction_price
            elif transaction.transaction_type == 'sell':
                crypto_holdings[crypto] -= transaction.amount
                total_value -= transaction.amount * transaction.transaction_price
                total_gain_loss += transaction.amount * transaction.transaction_price

        history_data = {
            'total_value': f'{total_value} $',
            'total_gain_loss': f'{total_gain_loss}  $',
            'crypto_holdings': crypto_holdings
        }

        return jsonify(history_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500