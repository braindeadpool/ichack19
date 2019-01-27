import os
import json
import subprocess
import multiprocessing
import argparse
from flask import Flask, flash, request, redirect, url_for, jsonify, session
from werkzeug.utils import secure_filename
from copy import deepcopy
import logging
import time
from frameanalysis import *
from collections import deque

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
FACE_BINARY_PATH = os.path.join('/Users/suraj_personal/projects/drishti/_builds/src/app/face/Release/drishti-face')
ASSETS_PATH = os.path.join('/Users/suraj_personal/projects/drishti-assets/drishti_assets_full.json')
BASE_ARGS = [FACE_BINARY_PATH, '-F', ASSETS_PATH, '-p', '--inner', '-i']
UPLOAD_DIR = os.path.join('/Users/suraj_personal/projects/ichack19/temp_dir')
MAX_NUM_PROCESSES = 20

DEFAULT_JSON_RESPONSE = {'Success': False,
    'Face' : None,
    'DebugInfo': 'INVALID_REQUEST',
    }


# EYE POSITIONS TO WORD CONVERSION
# define two constants, one for the eye aspect ratio to indicate
# blink and then a second constant for the number of consecutive
# frames the eye must be below the threshold
EYE_AR_THRESH = 0.35
EYE_AR_CONSEC_FRAMESshort = 3
#EYE_AR_CONSEC_FRAMESlong=10
confirm=15

LONG_WINDOW = 15
SHORT_WINDOW = 3
last_responses = deque(maxlen=LONG_WINDOW)

# initialize the frame counters and the total number of blinks,left and right 
COUNTERblink = 0
COUNTERfail = 0
COUNTERleft=0
COUNTERright=0
TOTALblink = 0
TOTALleft=0
TOTALright=0
#totallong=0
word=[]
blink_added = False


# *****************************************************************************************   
#NOW ENTER THE CODE TO RUN ON THE DRISHTI HERE> AT THE END SHOULD GIVE A JSON FILE 
#return response 
#where response is the JSON file
# *****************************************************************************************


def parse_response(response):
    global EYE_AR_THRESH, EYE_AR_CONSEC_FRAMESshort, confirm
    global COUNTERblink, COUNTERleft, COUNTERright, COUNTERfail, TOTALblink, TOTALleft, TOTALright, word, blink_added


    if response['Success']:
        # coordinates to compute the eye aspect ratio for both eyes
        leftEAR = eye_aspect_ratio_left(response)
        rightEAR = eye_aspect_ratio_right(response)

        logging.debug(f"lEAR = {leftEAR}")
        logging.debug(f"rEAR = {rightEAR}")

        # average the eye aspect ratio together for both eyes
        ear = (leftEAR + rightEAR) / 2.0

        # check to see if the eye aspect ratio is below the blink
        # threshold, and if so, increment the blink frame counter
        if ear < EYE_AR_THRESH:
            last_responses.append(1)
        elif l_or_r(response)=="left":
            last_responses.append(2)
                
        elif l_or_r(response) == "right":
            last_responses.append(3)
    else: 
        last_responses.append(0)

    logging.debug(f"Full window = {list(last_responses)}")
    if len(last_responses) % SHORT_WINDOW == 0 and len(last_responses) >= SHORT_WINDOW:
        short_responses = list(last_responses)[-SHORT_WINDOW:]
        logging.debug(f"Parsed Short window = {short_responses}")
        if short_responses.count(short_responses[0]) == SHORT_WINDOW and short_responses[0] != 0:
            word.append(short_responses[0])
        if last_responses.count(1) == LONG_WINDOW or last_responses.count(0) == LONG_WINDOW:
            # last_responses.clear()
            word = []
        logging.debug(f"Message = {word}")
    
    response['Message'] = word
    return response


def update_counters(results):
    global COUNTERblink, COUNTERleft, COUNTERright, TOTALblink, TOTALleft, TOTALright, word
    for response in results:
        parse_response(response)
        logging.debug(f"Current message = {word}")
        response['Message'] = word
    return results


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

def process_single_file(file, api_response_start_time):
    json_data = deepcopy(DEFAULT_JSON_RESPONSE)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        image_save_path = os.path.join(UPLOAD_DIR, filename)
        file.save(image_save_path)
        json_data = frame_to_face_contours(image_save_path, UPLOAD_DIR, api_response_start_time)
    else:
        json_data["DebugInfo"] = "BINARY_FAILED_ON_SINGLE_IMAGE"
    return json_data

def process_single_file_parallel(image_save_path):
    logging.debug(f"Starting parallel process for file at {image_save_path}")
    api_response_start_time = time.time()
    return frame_to_face_contours(image_save_path, UPLOAD_DIR, api_response_start_time)

@app.route('/api/image_to_eye_letters/', methods=['POST', 'GET'])
def process_image(request):
    api_response_start_time = time.time()
    json_data = deepcopy(DEFAULT_JSON_RESPONSE)
    if request.method == 'POST':
        logging.debug(request.files)
        # check if the post request has the file part
        if 'file' not in request.files:
            logging.debug("No file in request.files")
            json_data['DebugInfo'] = 'NO_FILE_IN_POST_REQUEST'
            return jsonify(json_data)
        file = request.files['file']
        logging.debug(file)
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            logging.debug("No selected file")
            json_data['DebugInfo'] = 'INVALID_FILENAME_IN_POST_REQUEST'
            return jsonify(json_data)
        return jsonify(process_single_file(file, api_response_start_time))
        
    else:
        logging.debug("Not post request")
        json_data['DebugInfo'] = 'NOT_POST_REQUEST'
        return jsonify(json_data)

@app.route('/api/images_to_eye_letters/', methods=['POST', 'GET'])
def process_images():
    api_response_start_time = time.time()
    json_data = deepcopy(DEFAULT_JSON_RESPONSE)
    if request.method == 'POST':
        logging.debug(request.files)
        # check if the post request has the file part
        if 'file' not in request.files:
            logging.debug("No file in request.files")
            json_data['DebugInfo'] = 'NO_FILE_KEY_IN_POST_REQUEST'
            return jsonify(json_data)
        files = request.files.getlist("file")
        parallel_queue = []
        for idx, file in enumerate(files):
            if file.filename == '':
                flash('No selected file')
                logging.debug("No selected file")
                json_data['DebugInfo'] = 'INVALID_FILENAME_IN_POST_REQUEST'
                return jsonify(json_data)
            else:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    basename, ext = os.path.splitext(filename)
                    filename = basename + f"_{idx}_{round(time.time()*100000)}" + ext
                    image_save_path = os.path.join(UPLOAD_DIR, filename)
                    file.save(image_save_path)
                parallel_queue.append(image_save_path)
        pool_size = min(len(files), MAX_NUM_PROCESSES)
        with multiprocessing.Pool(pool_size) as pool:
            logging.debug(f"Created pool of size {pool_size}")
            results = pool.map(process_single_file_parallel, parallel_queue)
        results = update_counters(results)
        return jsonify(results)
    else:
        logging.debug("Not post request")
        json_data['DebugInfo'] = 'NOT_POST_REQUEST'
        return jsonify(json_data)

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
