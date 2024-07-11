from flask import Blueprint, request, jsonify, session
from Backend.src.models import Transaction
from Backend.src.extensions import db
from flask_jwt_extended import jwt_required
from Backend.src.models import PortfolioHistory


transaction_routes = Blueprint('transactions', __name__)


@transaction_routes.route('/transactions', methods=["POST"])
@jwt_required()
def add_transaction():
    try:
        data = request.get_json()
        session['last_transaction'] = data
        print("Session data set:", session['last_transaction'])  # Debugging print

        transaction = Transaction(
            user_id=data['user_id'],
            cryptocurrency=data['cryptocurrency'],
            amount=data['amount'],
            transaction_type=data['transaction_type'],
            transaction_price=data['transaction_price']
        )
        db.session.add(transaction)
        db.session.commit()
        return jsonify({'message': 'Transaction was made successfully'}), 201
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
        db.session.commit()  # Corrected typo from db.session.commir()
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
    session_data = dict(session)  # Retrieve session data
    return jsonify(session_data), 200


@transaction_routes.route('/transactions/history', methods=['POST'])
@jwt_required()
def add_historical_data():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        date = data.get('date')
        value = data.get('value')

        history = PortfolioHistory(user_id=user_id, date=date, value=value)
        db.session.add(history)
        db.session.commit()
        return jsonify({'message': 'Portfolio history added'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@transaction_routes.route('/transactions/history', methods=['GET'])
@jwt_required()
def get_historical_data():
    try:
        user_id = request.args.get('user_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        query = PortfolioHistory.query
        if user_id:
            query = query.filter(PortfolioHistory.user_id == user_id)
        if start_date:
            query = query.filter(PortfolioHistory.date >= start_date)
        if end_date:
            query = query.filter(PortfolioHistory.date <= end_date)

        transactions = query.all()
        history_data = [transaction.as_dict() for transaction in transactions]

        return jsonify(history_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
