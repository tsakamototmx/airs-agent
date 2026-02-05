import requests
import traceback
import json
import logging
import boto3

ssm = boto3.session.Session().client(service_name="ssm", region_name='us-east-1')
logger = logging.getLogger(__name__)
profile = "pae-sec-profile-01"


def request_airs(prompt):
    try:
        res = ssm.get_parameter(
            Name='/airs/key',
            WithDecryption=True
        )
        res_json = json.loads(res['Parameter']['Value'])
        
        airs_url = res_json["url"]
        key = res_json["key"]

        json_object = {
            "contents": [
                {
                    "prompt": prompt
                }
            ],
            "ai_profile": {
                "profile_name": profile
                },
            "metadata": {
                    "ai_model": "Test AI model",
                    "app_name": "pae-app-01", 
                    "app_user": "test-user-1"
            },
            "tr_id": "1234"
        }

        header = {'x-pan-token': key}

        airs_response = requests.post(airs_url, json = json_object, headers = header)
        json_data = json.loads(airs_response.text)
        #recommendedAction = json_data['action']
        #print("The recommended action for this prompt is: " + recommendedAction + ".")
        return json_data
    except Exception:
        error_msg = traceback.format_exc()
        return
