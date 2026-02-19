import os
import json
from django.http import JsonResponse
from http import HTTPStatus
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.views.decorators.http import require_http_methods
import csv
import subprocess
import sys
import cloudinary
import cloudinary.uploader
import time
from .models import VisionGraph
from .utils import check_auth

HTML_DIR = 'ti14-vision/data'
EVENTS_DATA_DIR = 'ti14-vision/output'
VISION_GRAPH_DIR = 'ti14-vision/output'

@require_http_methods(["GET"])
def match_events(request):
    # check auth token
    check_auth_response = check_auth(request);
    if not check_auth_response[0]:
        return JsonResponse({'message': check_auth_response[1]}, status=HTTPStatus.UNAUTHORIZED)

    # validate parameters
    match_id = request.GET.get('match_id')
    if match_id is None:
        return JsonResponse({'message': 'match_id parameter is required'}, status=HTTPStatus.BAD_REQUEST)

    # generate events csv data (through third-party tool) if it's not generated
    events_data_file_path = f'{EVENTS_DATA_DIR}/events_{match_id}.csv'
    if not os.path.isfile(events_data_file_path):
        try:
            generate_match_data(match_id)
        except Exception as ex:
            print(f'Internal error: {ex}')
            return JsonResponse({'message':'Failed to get events data for the selected match. Please make sure the match ID is valid.'}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
    
    # process events csv data
    with open(events_data_file_path, mode='r', newline='') as file:
        csv_dict_reader = csv.DictReader(file)
        events_data = []
        for row in csv_dict_reader:
            events_data.append(row)

        return JsonResponse({'events':events_data}, status=HTTPStatus.OK)

@require_http_methods(["GET"])
def match_vision_graph(request):
    # check auth token
    check_auth_response = check_auth(request);
    if not check_auth_response[0]:
        return JsonResponse({'message': check_auth_response[1]}, status=HTTPStatus.UNAUTHORIZED)

    # validate parameters
    match_id = request.GET.get('match_id')
    enemy_side = request.GET.get('enemy_side')
    
    if match_id is None:
        return JsonResponse({'message': 'match_id parameter is required'}, status=HTTPStatus.BAD_REQUEST)

    if enemy_side is None:
        return JsonResponse({'message': 'enemy_side parameter is required'}, status=HTTPStatus.BAD_REQUEST)
    
    # return vision graph url directly if vision graph is already generated/uploaded
    vision_graph_id = f'enemy_{enemy_side}_{match_id}'
    try:
        vision_graph_object = VisionGraph.objects.get(vision_graph_id=vision_graph_id)
        return JsonResponse({'url': vision_graph_object.url}, status=HTTPStatus.OK)
    except VisionGraph.DoesNotExist:
        print(f'Vision graph {vision_graph_id} does not exist')

    # generate vision graph
    vision_graph_file_path = f'{VISION_GRAPH_DIR}/{vision_graph_id}.jpg'
    if not os.path.isfile(vision_graph_file_path):
        if enemy_side == 'Dire':
            our_side = 'Radiant'
        else:
            our_side = 'Dire'
        try:
            generate_match_data(match_id, our_side)
        except Exception:
            return JsonResponse({'message':'Server encountered an internal error'}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
    
    # upload vision graph
    upload_response = upload_vision_graph(vision_graph_file_path, vision_graph_id)

    # save uploaded vision graph url to database
    VisionGraph.objects.create(vision_graph_id=vision_graph_id, 
                               url=upload_response['secure_url'], 
                               date_created=upload_response['created_at'])
    print(f'upload_response:{upload_response}')

    return JsonResponse({'url': upload_response['secure_url']}, status=HTTPStatus.OK)

def get_html_file_name(match_id):
    return f'{HTML_DIR}/Match {match_id} - Vision - DOTABUFF - Dota 2 Stats.html'

def download_html(match_id):
    html_file_path = get_html_file_name(match_id)
    print(f'Download html for {match_id} to {html_file_path}')
    if not os.path.isfile(html_file_path):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.140 Safari/537.36"
        chrome_options.add_argument("user-agent={}".format(user_agent))

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(f'https://www.dotabuff.com/matches/{match_id}/vision')

        with open(html_file_path, "w", encoding='utf-8') as file:
            file.write(driver.page_source)

def generate_match_data(match_id, our_side='Dire'):
    if not os.path.isfile(get_html_file_name(match_id)):
        download_html(match_id)

    command = [
        sys.executable,
        'single_game_vision.py',
        '--game_id', match_id,
        '--our_side', our_side
    ]
    try:
        result = subprocess.run(command, 
                                cwd='ti14-vision',
                                capture_output=True, 
                                text=True, 
                                check=True)
        print("Target script output:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running target script: {e}")
        print(f"Stderr: {e.stderr}")
        raise e

def upload_vision_graph(vision_graph_file_path, vision_graph_id):

    cloudinary.config(
        cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key = os.getenv("CLOUDINARY_API_KEY"),
        api_secret = os.getenv("CLOUDINARY_API_SECRET")
    )

    timestamp = int(time.time())
    params_to_sign = {
        "timestamp": timestamp,
        "public_id": vision_graph_id
    }

    signature = cloudinary.utils.api_sign_request(params_to_sign, cloudinary.config().api_secret)

    upload_response = cloudinary.uploader.upload(
        vision_graph_file_path,
        type='private',
        api_key=cloudinary.config().api_key,
        signature=signature,
        timestamp=timestamp,
        public_id=vision_graph_id
    )
    print(upload_response)
    return upload_response