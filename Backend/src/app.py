from Backend.src import create_app
import logging

app = create_app()
logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    app.run(debug=True)


