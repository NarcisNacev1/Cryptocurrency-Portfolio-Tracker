from flask import Blueprint, jsonify
from Backend.src.models import Transaction
from Backend.src.services.crypto import get_crypto_prices
from decimal import Decimal


portfolio_routes = Blueprint('portfolio', __name__)


@portfolio_routes.route('/portfolio', methods=['GET'])
def get_portfolio_value():
    try:
        transactions = Transaction.query.all()
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

        return jsonify({'total_value': str(total_value) + ' $ '})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@portfolio_routes.route('/portfolio/advanced', methods=['GET'])
def get_advanced_portfolio_value():
    try:
        transactions = Transaction.query.yield_per(100)
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