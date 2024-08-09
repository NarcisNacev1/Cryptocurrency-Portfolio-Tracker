from flask import Blueprint, jsonify
from Backend.src.models import Transaction, User
from Backend.src.services.crypto import get_crypto_prices
from decimal import Decimal
from flask_jwt_extended import get_jwt_identity, jwt_required

portfolio_routes = Blueprint('portfolio', __name__)

@portfolio_routes.route('/portfolio', methods=['GET'])
@jwt_required()
def get_portfolio_value():
    try:
        #For Individual Prices Of the Cryptos it goes fetches the username of the user then querys the table then takes the id of the user and then gets the transactopons for it
        current_user = get_jwt_identity()
        current_username = current_user['username']

        user = User.query.filter_by(username=current_username).first()
        if not user:
            return jsonify({'msg': 'User not found'}), 404

        current_user_id = user.id
        transactions = Transaction.query.filter_by(user_id=current_user_id).all()
        cryptos = [transaction.as_dict() for transaction in transactions]

        #for total value
        portfolio = {}
        for transaction in transactions:
            crypto = transaction.cryptocurrency
            if crypto not in portfolio:
                portfolio[crypto] = Decimal('0')
            if transaction.transaction_type == 'buy':
                portfolio[crypto] += transaction.amount
            elif transaction.transaction_type == 'sell':
                portfolio[crypto] -= transaction.amount

        total_value = Decimal('0')
        for crypto, amount in portfolio.items():
            try:
                current_price = Decimal(str(get_crypto_prices(crypto)))
                total_value += amount * current_price
            except KeyError:
                return jsonify({'error': f"Current price for {crypto} not found in API response."}), 404
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        return jsonify({'Indevidual_Cryptos': cryptos ,'Total_Value': str(total_value) + ' $ '})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@portfolio_routes.route('/portfolio/advanced', methods=['GET'])
@jwt_required()
def get_advanced_portfolio_value():
    try:
        current_user = get_jwt_identity()
        current_username = current_user['username']

        user = User.query.filter_by(username=current_username).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        transactions = Transaction.query.filter_by(user_id=user.id).yield_per(100)
        portfolio = {}
        for transaction in transactions:
            crypto = transaction.cryptocurrency
            if crypto not in portfolio:
                portfolio[crypto] = Decimal('0')
            if transaction.transaction_type == 'buy':
                portfolio[crypto] += transaction.amount
            elif transaction.transaction_type == 'sell':
                portfolio[crypto] -= transaction.amount

        total_value = Decimal('0')
        for crypto, amount in portfolio.items():
            try:
                current_price = get_crypto_prices(crypto)
                total_value += amount * current_price
            except KeyError:
                return jsonify({'error': f"Current price for {crypto} not found in API response."}), 404
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        return jsonify({'total_value': str(total_value) + ' $ '})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
