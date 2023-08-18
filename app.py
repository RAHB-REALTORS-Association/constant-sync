from datetime import datetime
from flask import Flask, render_template
from threading import Thread
from synchronizer import synchronize_contacts
from scheduler import start_scheduled_synchronization
from oauth2 import oauth2_blueprint
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__, static_url_path='/static')
app.register_blueprint(oauth2_blueprint)
app.secret_key = 'some_secure_random_string'  # Please use a secure secret key in production

# Global variable to hold last sync status
last_sync_status = None

@app.route('/')
def index():
    return render_template('index.html', last_sync=last_sync_status)

@app.route('/manual_sync', methods=["POST"])
def manual_sync():
    global last_sync_status
    try:
        synchronize_contacts()
        last_sync_status = f"Last successful sync at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        return render_template('sync_success.html')
    except Exception as e:
        last_sync_status = f"Error during sync at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {str(e)}"
        return render_template('error.html', error_message=f"Error during manual synchronization: {e}")

if __name__ == '__main__':
    # Start synchronization service as a background thread
    sync_thread = Thread(target=start_scheduled_synchronization)
    sync_thread.start()

    logging.info("Starting Flask application...")
    app.run(debug=True)
