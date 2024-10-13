from flask import Flask, request, jsonify
import json
import os
import subprocess
import time
from datetime import datetime
import asyncio
import v2iplimit

app = Flask(__name__)

CONFIG_FILE = 'config.json'
LOG_FILE = 'cronjob_log.log'
SCRIPT_PATH = 'v2iplimit.py'
TOKEN = 'AaaaaahhhhhhhhAaaaaaaNaaasiiiiiirrrrrYavashhhhhhhhhhhhhhh'

def load_config():
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def log(message):
    with open(LOG_FILE, 'a') as f:
        f.write(f"{message}\n")

def terminate_existing_processes():
    log(f"Script executed at {datetime.now()}")
    log("Terminating existing instances of v2iplimit.py")

    try:
        pids = subprocess.check_output(["pgrep", "-f", "v2iplimit.py"]).decode().strip().split()
        if pids:
            log(f"Existing process IDs: {pids}")
            for pid in pids:
                log(f"Killing process {pid}")
                os.kill(int(pid), 9)
            time.sleep(5)
            pids = subprocess.check_output(["pgrep", "-f", "v2iplimit.py"]).decode().strip().split()
            log(f"Remaining process IDs: {pids}")
    except subprocess.CalledProcessError:
        log("No existing process found.")

def start_new_process():
    log("Starting v2iplimit.py")
    subprocess.Popen(["python", SCRIPT_PATH])
    #v2iplimit.main()

@app.route('/update_special_limit', methods=['POST'])
def update_special_limit():
    data = request.get_json()
    user = data.get('user')
    limit = data.get('limit')
    token = data.get('token')

    if token == TOKEN:
        if not user or not isinstance(limit, int):
            return jsonify({'error': 'Invalid input'}), 400

        config = load_config()

        # Check if the user exists in SPECIAL_LIMIT
        special_limit = config.get('SPECIAL_LIMIT', [])
        for i, (existing_user, existing_limit) in enumerate(special_limit):
            if existing_user == user:
                special_limit[i] = [user, limit]
                config['SPECIAL_LIMIT'] = special_limit
                save_config(config)
                terminate_existing_processes()
                start_new_process()
                return jsonify({'status': 'updated'}), 200

        # If user does not exist, add to SPECIAL_LIMIT
        special_limit.append([user, limit])
        config['SPECIAL_LIMIT'] = special_limit
        save_config(config)
        terminate_existing_processes()
        start_new_process()
        return jsonify({'status': 'added'}), 201
    elif not user or not token or not limit or not isinstance(limit, int):
        return jsonify({'message': 'fuck you! you are not the admin go fuck off son of a bitch'}), 403
    elif token != TOKEN:
        return jsonify({'message': 'hahaha kir khordi tokenet ride'})

if __name__ == '__main__':
    terminate_existing_processes()
    start_new_process()
    app.run(port = int(os.environ.get('PORT', 5000)),debug=True)
