import sys
import json
import time
import socket
import threading
import os
from flask import Flask, jsonify
from flask_cors import CORS

# --- Config ----
# Read host and port from environment variables, with defaults.
DUMP1090_HOST = os.getenv("DUMP1090_HOST", "localhost")
DUMP1090_PORT = int(os.getenv("DUMP1090_PORT", 30003))
FR24BACK_LOG_UPDATE = int(os.getenv("FR24BACK_LOG_UPDATE", 300))
# Read debug mode on / off
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() in ('true', '1', 't')

FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000

# Time in seconds to remove an airplane from the live airplane list
DATA_EXPIRATION_SECONDS = 300  # 300 seconds / 5 minutes

# --- In-memory data of nearby airplanes ---
aircraft_data = {}
# Use a lock to prevent concurrency issues when accessing data
# from both the parser thread and the web server thread.
data_lock = threading.Lock()


# --- Thread for dump1090 ---
def sbs_parser_thread():
    """This thread connects to dump1090, parses the data, and updates it."""
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((DUMP1090_HOST, DUMP1090_PORT))
                print(f"Connected to dump1090 at {DUMP1090_HOST}:{DUMP1090_PORT}")
                buffer = ""
                while True:
                    data = s.recv(1024).decode('utf-8', 'ignore')
                    if not data:
                        break

                    buffer += data
                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        parse_sbs1_message(line)

        except (socket.error, ConnectionRefusedError) as e:
            print(f"Connection error with dump1090: {e}. Retrying in 5 seconds...")
            time.sleep(5)
        except KeyboardInterrupt:
            break


def parse_sbs1_message(message):
    """Parses an SBS-1 message and updates the aircraft dictionary."""
    parts = message.strip().split(',')
    if not parts or len(parts) < 5 or parts[0] != 'MSG':
        return

    icao_hex = parts[4]
    msg_type = parts[1]

    with data_lock:
        if icao_hex not in aircraft_data:
            aircraft_data[icao_hex] = {'icao': icao_hex}

        aircraft = aircraft_data[icao_hex]
        aircraft['last_seen'] = time.time()

        # Update data based on message type (with error handling)
        try:
            if msg_type == '1' and len(parts) > 10 and parts[10]:
                aircraft['callsign'] = parts[10].strip()
            elif msg_type == '2':  # Surface position
                if len(parts) > 11 and parts[11]: aircraft['altitude'] = int(parts[11])
                if len(parts) > 12 and parts[12]: aircraft['ground_speed'] = int(parts[12])
                if len(parts) > 13 and parts[13]: aircraft['track'] = int(parts[13])
            elif msg_type == '3':  # Airborne position
                if len(parts) > 11 and parts[11]: aircraft['altitude'] = int(parts[11])
                if len(parts) > 14 and parts[14]: aircraft['lat'] = float(parts[14])
                if len(parts) > 15 and parts[15]: aircraft['lon'] = float(parts[15])
            elif msg_type == '4':  # Airborne velocity
                if len(parts) > 12 and parts[12]: aircraft['ground_speed'] = int(parts[12])
                if len(parts) > 13 and parts[13]: aircraft['track'] = int(parts[13])
                if len(parts) > 16 and parts[16]: aircraft['vertical_rate'] = int(parts[16])
            elif msg_type == '5' and len(parts) > 21 and parts[21]:
                if parts[21]: aircraft['on_ground'] = bool(int(parts[21]))
            elif msg_type == '6' and len(parts) > 17 and parts[17]:
                aircraft['squawk'] = parts[17]
        except (ValueError, IndexError):
            # Ignore malformed data in a specific message
            pass


def cleanup_old_aircraft():
    """Removes aircraft from the dictionary that have not been seen recently."""
    now = time.time()
    with data_lock:
        # We create a list of ICAOs to remove so as not to modify the dictionary while iterating
        to_remove = [icao for icao, data in aircraft_data.items() if
                     now - data.get('last_seen', now) > DATA_EXPIRATION_SECONDS]
        for icao in to_remove:
            del aircraft_data[icao]
            print(f"Removed inactive aircraft: {icao}")


def cleanup_thread():
    """Periodically cleans up old aircraft data."""
    while True:
        cleanup_old_aircraft()
        time.sleep(15)

def log_aircraft_count_thread():
    """Periodically logs the number of aircraft being tracked."""
    while True:
        time.sleep(FR24BACK_LOG_UPDATE)
        with data_lock:
            count = len(aircraft_data)
        print(f"Total aircraft being tracked: {count}")

# --- Flask Server ---
app = Flask(__name__)
# Enable CORS, restricting it to specific origins for security.
# This allows requests from your production domain and from the local development server.
origins = ["https://vuelos.kmc.ar", "http://localhost:8080"]
CORS(app, resources={r"/api/*": {"origins": origins}})


@app.route('/api/flights')
def get_flights():
    """Endpoint that returns current flight data."""
    with data_lock:
        # We return a list of the dictionary's values, not the entire dictionary,
        # so that the JSON is an array of objects, which is more standard for APIs.
        return jsonify(list(aircraft_data.values()))


# --- Main entry point ---
if __name__ == '__main__':
    print(f"Starting the thread to process data from dump1090 on ip={DUMP1090_HOST} and port={DUMP1090_PORT}")
    parser = threading.Thread(target=sbs_parser_thread, daemon=True)
    parser.start()

    print("Starting the cleanup thread...")
    cleaner = threading.Thread(target=cleanup_thread, daemon=True)
    cleaner.start()

    print("Starting the aircraft count logging thread...")
    logging_thread = threading.Thread(target=log_aircraft_count_thread, daemon=True)
    logging_thread.start()

    print(f"Starting Flask server at http://{FLASK_HOST}:{FLASK_PORT}")
    print("Make sure you have the libraries installed: pip install Flask Flask-Cors")
    # We use 'threaded=True' so that Flask handles multiple requests at once
    app.run(host=FLASK_HOST, port=FLASK_PORT, threaded=True, debug=DEBUG_MODE)
