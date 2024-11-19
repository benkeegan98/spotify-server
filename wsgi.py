from app import create_app

app = create_app()
import logging
logging.basicConfig(level=logging.INFO)
logging.info("WSGI app initialized")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
