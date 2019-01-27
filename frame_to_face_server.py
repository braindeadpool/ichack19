import os
import json
import subprocess
import argparse
from flask import Flask, flash, request, redirect, url_for, jsonify, session
from werkzeug.utils import secure_filename
from copy import deepcopy
import logging
import time

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
FACE_BINARY_PATH = os.path.join('/Users/suraj_personal/projects/drishti/_builds/src/app/face/Release/drishti-face')
ASSETS_PATH = os.path.join('/Users/suraj_personal/projects/drishti-assets/drishti_assets_full.json')
BASE_ARGS = [FACE_BINARY_PATH, '-F', ASSETS_PATH, '-a', '-p', '--inner', '-i']
UPLOAD_DIR = os.path.join('/Users/suraj_personal/projects/ichack19/temp_dir')

DEFAULT_JSON_RESPONSE = {'Success': False,
    'Face' : None,
    'DebugInfo': 'NOT_POST_REQUEST',
    }

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def _clean_face_json(json_data):
    """
    clean the json output from Drishti binary
    """
    json_data['faces'][0].pop("cereal_class_version")
    json_data['faces'][0]["eye-full-left"].pop("cereal_class_version")
    json_data['faces'][0]["eye-full-left"]["value1"].pop("cereal_class_version")
    json_data['faces'][0]["eye-full-left"]["value1"]["roi"].pop("cereal_class_version")
    json_data['faces'][0]["eye-full-left"]["value1"]["roi"]["value1"].pop("cereal_class_version")
    json_data['faces'][0]["eye-full-left"]["value1"]["eyelids"][0].pop("cereal_class_version")
    json_data['faces'][0]["eye-full-left"]["value1"]["iris"].pop("cereal_class_version")
    json_data['faces'][0]["eye-full-left"]["value1"]["iris"]["size"].pop("cereal_class_version")
    json_data['faces'][0]["eye-full-left"]["value1"]["inner"].pop("cereal_class_version")
    return json_data

@app.route('/')
def index():
    return "<h1>Eye2Action</h1>"

@app.route('/api/image_to_eye_letters/', methods=['POST', 'GET'])
def process_image():
    api_response_start_time = time.time()
    if request.method == 'POST':
        logging.debug(request.files)
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            logging.debug("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            image_save_path = os.path.join(UPLOAD_DIR, filename)
            file.save(image_save_path)
            json_data = frame_to_face_contours(image_save_path, UPLOAD_DIR, api_response_start_time)
            return jsonify(json_data)
    return jsonify(DEFAULT_JSON_RESPONSE)

def frame_to_face_contours(image_path, output_dir, api_response_start_time):
    face_binary_start = time.time()
    command_output = subprocess.check_output(BASE_ARGS+[image_path, '-o', output_dir], stderr=subprocess.STDOUT)
    face_binary_end = time.time()
    logging.debug(f"Face binary command took {face_binary_end-face_binary_start} seconds")
    logging.debug(command_output)
    output_path = os.path.splitext(image_path)[0]+'.json'
    json_response = DEFAULT_JSON_RESPONSE.copy()
    if os.path.isfile(output_path):
        with open(output_path, 'r') as f:
            json_data = json.load(f)
            json_response['Success'] = True
            json_response['Face'] = deepcopy(_clean_face_json(json_data))
            json_response['DebugInfo'] = {'Timing': {'FaceBinary': face_binary_end-face_binary_start,
            'ServerResponse': time.time()-api_response_start_time}}
    else:
        json_response['DebugInfo'] = {'Timing': {'ServerResponse': time.time()-api_response_start_time}}
    return json_response

def main():
    global UPLOAD_DIR
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--port', default=8090, type=int,
                        help='Port to start flask server')
    parser.add_argument('-f','--file-dir', default=UPLOAD_DIR,
                        help='Directory to store and process files during web requests')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose debug messages')
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    os.makedirs(args.file_dir, exist_ok=True)
    UPLOAD_DIR = args.file_dir
    app.config['SESSION_TYPE'] = 'filesystem'
    app.secret_key = 'super secret key'
    
    app.run(host="0.0.0.0", port=args.port)


if __name__ == "__main__":
    main()
