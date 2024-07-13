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

### Setup

1. **Clone the repository:**
    ```sh
    git clone https://github.com/NarcisNacev1/Cryptocurrency-Portfolio-Tracker.git
    cd Cryptocurrency-Portfolio-Tracker
    ```

2. **Create a virtual environment and activate it:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Configure the environment variables:**
    - Create a `.env` file in the root directory and add the following lines:
        ```sh
        FLASK_APP=Backend.src
        FLASK_ENV=development
        ```

5. **Set up the database:**
    - Replace the following line in your configuration file with your database details:
        ```python
        SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@host:port/database_name'
        ```
    - Run the following commands to initialize and migrate the database:
        ```sh
        flask db init
        flask db migrate -m "Initial migration"
        flask db upgrade
        ```

### Running the Application

1. **Start the Flask server:**
    ```sh
    flask run
    ```

2. **Open Postman and use the following routes to interact with the API:**

    - **Register a new user:**
        - **URL:** `http://127.0.0.1:5000/register`
        - **Method:** POST
        - **Body:**
            ```json
            {
                "username": "Marko",
                "password": "555555"
            }
            ```

    - **Login:**
        - **URL:** `http://127.0.0.1:5000/login`
        - **Method:** POST
        - **Body:**
            ```json
            {
                "username": "Marko",
                "password": "555555"
            }
            ```
        - **Note:** Upon successful login, you will receive an authorization token which should be included in the headers for subsequent requests:
            ```
            Authorization: Bearer <token>
            ```

    - **Add a transaction:**
        - **URL:** `http://127.0.0.1:5000/transactions`
        - **Method:** POST
        - **Body:**
            ```json
            {
                "user_id": "2",
                "cryptocurrency": "dogecoin",
                "amount": "1",
                "transaction_type": "buy",
                "transaction_price": "55"
            }
            ```

    - **View transactions:**
        - **URL:** `http://127.0.0.1:5000/transactions`
        - **Method:** GET

    - **Add portfolio value history:**
        - **URL:** `http://127.0.0.1:5000/transactions/history`
        - **Method:** POST
        - **Body:**
            ```json
            {
                "user_id": "2",
                "date": "2023-07-10",
                "value": "3000"
            }
            ```

    - **View portfolio value history:**
        - **URL:** `http://127.0.0.1:5000/transactions/history`
        - **Method:** GET

    - **View session data:**
        - **URL:** `http://127.0.0.1:5000/session_data`
        - **Method:** GET

    - **View portfolio value:**
        - **URL:** `http://127.0.0.1:5000/portfolio`
        - **Method:** GET

    - **View advanced portfolio value:**
        - **URL:** `http://127.0.0.1:5000/portfolio/advanced`
        - **Method:** GET

    - **Delete a transaction:**
        - **URL:** `http://127.0.0.1:5000/transactions/delete/<transaction_id>`
        - **Method:** DELETE

    - **Delete all transactions:**
        - **URL:** `http://127.0.0.1:5000/transactions/delete/all`
        - **Method:** DELETE

    - **Update a transaction:**
        - **URL:** `http://127.0.0.1:5000/transactions/update/<transaction_id>`
        - **Method:** PUT
        - **Body:**
            ```json
            {
                "user_id": "2",
                "cryptocurrency": "bitcoin",
                "amount": "3",
                "transaction_type": "buy"
            }
            ```

## Additional Information
- **Postman Documentation:** The repository includes a Postman collection in the `documentation` folder. Import this collection into Postman to easily test the API endpoints.
- **Database Configuration:** If you encounter issues with the database, ensure that you have configured it correctly in the configuration file and that PostgreSQL is running on your machine.
- **Prepopulated PostgreSQL Data**: The repository includes PostgreSQL documentation with prepopulated data in the `documentation` folder. Use this to quickly set up your database with sample data.

### Troubleshooting
- If you face issues with the Flask application not being found, set the Flask app path using:
    ```sh
    $env:FLASK_APP="Backend.src"  # On Windows PowerShell
    export FLASK_APP=Backend.src  # On Unix-based systems
    ```

- To resolve database issues, make sure to initialize and migrate the database using the following commands:
    ```sh
    flask db init
    flask db migrate -m "Description of changes"
    flask db upgrade
    ```

Feel free to reach out if you encounter any issues or need further assistance.
