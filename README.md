# Cryptocurrency Portfolio Tracker

## Key Features
- Real-time cryptocurrency price updates using an external API.
- Functionality for users to add and manage (CRUD) cryptocurrency transactions.
- Portfolio valuation and performance metrics.
- Utilization of advanced Python features and PostgreSQL for data handling and storage.

## Tools and Technologies
- **Backend Framework:** Flask
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **External API:** CoinGecko API (or any preferred free cryptocurrency API)
- **Testing Tool:** Postman

## Instructions for Use

1. **Setting Up the Environment:**
   - Open your terminal and navigate to the project directory.
   - Set the Flask app path: `$env:FLASK_APP="Backend.src"` (Windows) or `export FLASK_APP=Backend.src` (Linux/Mac).
   - Install required dependencies: `pip install -r requirements.txt`.

2. **Running the Flask Application:**
   - Start the Flask server: `flask run`.
   - The server will be accessible at `http://127.0.0.1:5000`.

3. **Using Postman:**
   - Register an account: `POST http://127.0.0.1:5000/register`
     ```json
     {
       "username": "Marko",
       "password": "555555"
     }
     ```
     - This request now returns the ID of the newly registered user.

   - Log in: `POST http://127.0.0.1:5000/login`
     ```json
     {
       "username": "Marko",
       "password": "555555"
     }
     ```
     - This request returns an authorization token to use in subsequent requests. Add it in the Headers tab as `Bearer <token>`.

   - Add a transaction: `POST http://127.0.0.1:5000/transactions`
     ```json
     {
       "user_id": "2",
       "cryptocurrency": "dogecoin",
       "amount": "1",
       "transaction_type": "buy"
     }
     ```
     - The `transaction_price` field has been removed as prices are now fetched in real time.

   - View transactions: `GET http://127.0.0.1:5000/transactions`

   - View portfolio value: `GET http://127.0.0.1:5000/portfolio`
     - Returns the cryptocurrencies owned and the total value of the portfolio.

   - Advanced portfolio view: `GET http://127.0.0.1:5000/portfolio/advanced`
     - Expanded to include cryptocurrencies owned and the total value of the portfolio.

   - Delete a transaction: `DELETE http://127.0.0.1:5000/transactions/delete/<id>`

   - Delete all transactions: `DELETE http://127.0.0.1:5000/transactions/delete/all`

   - Update a transaction: `PUT http://127.0.0.1:5000/transactions/update/<id>`
     ```json
     {
       "user_id": "2",
       "cryptocurrency": "bitcoin",
       "amount": "3",
       "transaction_type": "buy"
     }
     ```

   - View last transaction: `GET http://127.0.0.1:5000/session_data`
     ```json
     {
       "last_transaction": {
         "amount": 2,
         "cryptocurrency": "bitcoin",
         "transaction_type": "sell",
         "user_id": 4
       }
     }
     ```

   - View top 20 cryptocurrency prices: `GET http://127.0.0.1:5000/prices`

   - View price of a specified cryptocurrency: `GET http://127.0.0.1:5000/prices/<crypto>`
     - New route to get the price of a specific cryptocurrency.

   - View historical transaction data: `GET http://127.0.0.1:5000/transactions/history`
     ```json
     {
       "start_date": "2023-01-01",
       "end_date": "2023-12-31"
     }
     ```
     - New route to get historical transaction data. Filters by start and end dates and returns total value, total gain/loss, and cryptocurrency holdings.

4. **Database Configuration:**
   - Configure PostgreSQL database in `config.py`:
     ```python
     SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@host:port/database_name'
     ```
   - Initialize and upgrade the database:
     ```bash
     flask db init
     flask db migrate -m "Initial migration"
     flask db upgrade
     ```

5. **API Documentation:**
   - Swagger UI documentation is updated to include authorization.

6. **PostgreSQL Documentation:**
   - Prepopulated PostgreSQL documentation is available in the `documentation` folder.

## Updated Features
1. Renamed Postman documentation to be more readable and accessible.
2. Fixed issue with users being able to make transactions with other users' IDs.
3. Added API documentation using Swagger UI with authorization.
4. Added a `/prices/<crypto>` route that provides the price of a specified cryptocurrency.
5. Expanded `/portfolio` and `/portfolio/advanced` routes to return owned cryptocurrencies and the total portfolio value.
6. Fixed issues with viewing other people's portfolios and transactions.
7. Added real-time portfolio value checking based on cryptocurrency prices.
8. Reinvented the transaction history to include gain and loss information.
9. Removed the `/transactions/history` POST route and added a `/transactions/history` GET route for retrieving historical transaction data.

For further assistance, refer to the documentation folder or open an issue on GitHub.
