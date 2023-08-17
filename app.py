from flask import Flask, render_template
from threading import Thread
from scheduler import start_scheduled_synchronization
from oauth2 import bp as oauth2_bp
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.register_blueprint(oauth2_bp)
app.secret_key = 'some_secure_random_string'  # Please use a secure secret key in production

@app.route('/')
def index():
    return render_template('index.html')

def run_sync_service():
    logging.info("Starting synchronization service...")
    start_scheduled_synchronization(2)  # Every 2 hours (this can be configured)

if __name__ == '__main__':
    # Start synchronization service as a background thread
    sync_thread = Thread(target=run_sync_service)
    sync_thread.start()

    logging.info("Starting Flask application...")
    app.run(debug=True)
