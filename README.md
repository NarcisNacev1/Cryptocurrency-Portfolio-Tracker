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
       "transaction_type": "buy",
       "transaction_price": "55"
     }
     ```

   - View transactions: `GET http://127.0.0.1:5000/transactions`

   - Post portfolio value: `POST http://127.0.0.1:5000/transactions/history`
     ```json
     {
       "user_id": "2",
       "date": "2023-07-10",
       "value": "3000"
     }
     ```

   - View portfolio value: `GET http://127.0.0.1:5000/portfolio`

   - Advanced portfolio view: `GET http://127.0.0.1:5000/portfolio/advanced`

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

   - View top 10 cryptocurrency prices: `GET http://127.0.0.1:5000/prices`

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
   - Swagger UI documentation is available for API endpoints.

6. **PostgreSQL Documentation:**
   - Prepopulated PostgreSQL documentation is available in the `documentation` folder.

## Updated Features
1. Renamed Postman documentation to be more readable and accessible.
2. Fixed issue with users being able to make transactions with other users' IDs.
3. Added API documentation using Swagger UI.
4. Added a `/prices` route that provides the top 10 prices of cryptocurrencies.
5. Unhardcoded cryptocurrency prices and implemented real-time fetching of prices from the CoinGecko API.

For further assistance, refer to the documentation folder or open an issue on GitHub.
