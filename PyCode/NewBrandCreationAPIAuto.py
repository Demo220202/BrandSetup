import json
# from textwrap import indent
import base64
from UserPackageAuto import *
from rdsConnect import *
import requests
from AzureTestingJSON import *
import urllib3
import argparse

def get_domain_on_env(env):

    if env == "prod":
        domain = "internal.zenarate.com"
    elif env == "beta":
        domain = "beta-internal.zenarate.com"
    elif env == "qa":
        domain = "qa-internal.zenarate.com"
    elif env == "qa2":
        domain = "qa2-internal.zenarate.com"
    else:
        domain = None

    return domain

def get_url_on_env(env, url):

    if env == "prod":
        return url
    elif env == "beta":
        return f"beta-{url}"
    elif env == "qa2":
        return f"qa2-{url}"
    elif env == "qa":
        return f"qa-{url}"
    elif env == "dev":
        return f"dev-{url}"


def brand_settings_data_json(brand_info_json, azure_infor_json, twilio_json):

    data_json = {
            "GENERAL_CONFIG": {
                "enabled": 0,
                "config_json": {
                    "url": brand_info_json["url"],
                    "logo": None,
                    "name": brand_info_json["brand_name"],
                    "bucket": brand_info_json["bucket"],
                    "enable_canvas": 0,
                    "send_to_support_form": "support@zenarate.com",
                    "team_name": brand_info_json["team_name"]
                },
                "allowed-actions": "read"
            },
            "BUCKET_REPO_CONFIG": {
                "enabled": 1,
                "config_json": {
                    "bucket_repo": "{}"
                },
                "allowed-actions": "read"
            },
            "PASSWORD_POLICY_CONFIG": {
                "enabled": 0,
                "config_json": {
                    "pwd_len": "12",
                    "pwd_expiry": 90,
                    "pwd_history": "8"
                },
                "allowed-actions": "read"
            },
            "LOGIN_FAIL_THROTTLE_DURATION_CONFIG": {
                "enabled": 0,
                "config_json": {
                    "login_failed_throttle_duration": "30"
                },
                "allowed-actions": "read"
            },
            "LOGIN_ATTEMPTS_CONFIG": {
                "enabled": 0,
                "config_json": {
                    "login_failed_max_attempts": "3"
                },
                "allowed-actions": "read"
            },
            "SEND_CRED_MAIL_CONFIG": {
                "enabled": True,
                "config_json": {},
                "allowed-actions": "read"
            },
            "STORY_PREVIEW_CONFIG": {
                "enabled": True,
                "config_json": {},
                "allowed-actions": "read"
            },
            "FEATURE_AVATAR_CONFIG": {
                "enabled": True,
                "config_json": {},
                "allowed-actions": "read"
            },
            "ZENARATE_GUIDE_CONFIG": {
                "enabled": True,
                "config_json": {
                    "zenarate_guide_username": "",
                    "zenarate_guide_user_email": ""
                },
                "allowed-actions": "read"
            },
            "BROWSER_CONFIG": {
                "enabled": 0,
                "config_json": {
                    "preferred_browser": "1,4",
                    "preffered_browser": "1,4"
                },
                "allowed-actions": "read"
            },
            "MYNOTES_CONFIG": {
                "enabled": True,
                "config_json": {},
                "allowed-actions": "read"
            },
            "RESOURCE_CONFIG": {
                "enabled": True,
                "config_json": {},
                "allowed-actions": "read"
            },
            "SCORECARD_CONFIG": {
                "enabled": True,
                "config_json": {},
                "allowed-actions": "read"
            },
            "SCREENSCIM_GUIDANCE_SPOKEN_CONFIG": {
                "enabled": True,
                "config_json": {},
                "allowed-actions": "read"
            },
            "MIC_BUTTON_CONFIG": {
                "enabled": True,
                "config_json": {},
                "allowed-actions": "read"
            },
            "SCREEN_SIM_CONFIG": {
                "enabled": True,
                "config_json": {},
                "allowed-actions": "read"
            },
            "INSIGHTS_CONFIG": {
                "enabled": True,
                "config_json": {},
                "allowed-actions": "read"
            },
            "MSSPEECH_CONFIG": {
                "enabled": 0,
                "config_json": {
                    "msspeech_key": azure_infor_json["msspeech_key"],
                    "msspeech_version": "v2",
                    "msspeech_endpoint": "westus",
                    "msspeech_subscription_type": "msspeech_subscription",
                    "msspeech_subscription_resources": "{}"
                },
                "allowed-actions": "read"
            },
            "GPT_CONFIG": {
                "enabled": True,
                "config_json": {
                    "chatgpt_resources": "{}"
                },
                "allowed-actions": "read"
            },
            "SPEECH_SYNTHESIS_CONFIG": {
                "enabled": True,
                "config_json": {},
                "allowed-actions": "read"
            },
            "LUIS_CONFIG": {
                "enabled": 0,
                "config_json": {
                    "luis_appId": True,
                    "luis_thresholds": "20",
                    "luis_subscription": azure_infor_json["luis_app_subscription"],
                    "luis_subscription_type": "luis_subscription",
                    "luis_authoring_resource": "",
                    "pr_luis_thresholds_diff": "20",
                    "luis_reporting_subscription": azure_infor_json["luis_reporting_subscription"],
                    "luis_subscription_resources": "{}"
                },
                "allowed-actions": "read"
            },
            "AZURE_CONFIG": {
                "enabled": 0,
                "config_json": {
                    "azure_account_name": azure_infor_json["azure_account_name"],
                    "azure_resource_group": azure_infor_json["resource_group"],
                    "azure_subscription_id": azure_infor_json["subscription_id"],
                    "azure_reporting_account": azure_infor_json["reporting_account_name"],
                },
                "allowed-actions": "read"
            },
            "SPEECH_RESOURCE_CONFIG": {
                "enabled": 0,
                "config_json": {
                    "Speech": f"[{azure_infor_json['speech_json']}]"
                },
                "allowed-actions": "read"
            },
            "OPEN_AI_RESOURCE_CONFIG": {
                "enabled": 0,
                "config_json": {
                    "Open_AI": f"[{azure_infor_json['open_ai_json']}]"
                },
                "allowed-actions": "read"
            },
            "LUIS_RESOURCE_CONFIG": {
                "enabled": 0,
                "config_json": {
                    "LUIS_Authoring": f"[{azure_infor_json['luis_authoring_json']}]",
                    "LUIS_Prediction": "None"
                },
                "allowed-actions": "read"
            },
            "CLU_CONFIG": {
                "enabled": 0,
                "config_json": {
                    "clu_resources": "{}",
                    "advance_clu_thresholds": "20",
                    "standard_clu_thresholds": "20",
                    "pr_advance_clu_thresholds_diff": "20",
                    "pr_standard_clu_thresholds_diff": "20"
                },
                "allowed-actions": "read"
            },
            "TWILIO_CONFIG": {
                "enabled": 0,
                "config_json": {
                    "twilio_account_id": twilio_json["twilio_account"],
                    "twilio_account_token": twilio_json["twilio_token"],
                },
                "allowed-actions": "read"
            },
            "RECORDING_PREFERENCE_CONFIG": {
                "enabled": 1,
                "config_json": {
                    "ivr_number": [
                        {
                            # "id": "dcd34k",
                            "type": 1,
                            "number": twilio_json["start_number"]
                        },
                        {
                            # "id": "ufsogv",
                            "type": 2,
                            "number": twilio_json["recorded_number"]
                        }
                    ],
                    "recording_preference": "1"
                },
                "allowed-actions": "read"
            },
            "PROFANITY_CONFIG": {
                "enabled": 0,
                "config_json": {
                    "profanity_filter": "removed",
                    "profanity_library": None
                },
                "allowed-actions": "read"
            },
        }

    return data_json

def btoa_encode(user_id):
    # The string you want to encode (similar to btoa() in JavaScript)
    original_string = str(user_id)

    # Encode the string to bytes using utf-8 encoding, then Base64-encode it
    encoded_bytes = base64.b64encode(original_string.encode('utf-8'))

    # Convert the bytes back to a string
    encoded_string = encoded_bytes.decode('utf-8')

    print(encoded_string)

    return encoded_string


def change_brand_settings(access_token, domain, account_id, user_id, role, updated_data):

    url = f"https://{domain}/zen-api/config-api/brand/new"

    request_id = btoa_encode(user_id)

    payload = json.dumps(updated_data)
    headers = {
        # 'Authorization': f'Bearer {access_token}',
        'Cookie': f'account_id={account_id};_loggedIn_id={user_id};_zenarate_id={user_id};_role_id={role};Z-Request-ID={request_id};central_jwt_token={access_token};PHPSESSID=abcd',
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload)
    print(json.dumps(response.json(), indent=2))
    if response.status_code == 200:
        print("Successfully changed brand settings.")
        return response.json()
    return None


def create_default_policy(env, brand_id):

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    url = f"https://{env}.zenarate.pvt/internal/zen-api/teams/v1/policy/create-default-policy"

    headers = {
        'x-api-key': f'{brand_id}',
        'x-user-id': "",
        'Content-Type': 'application/json'
    }

    payload = {}

    response = requests.post(url, headers=headers, json=payload, verify=False)

    print(json.dumps(response.json(), indent=2))

    if response.status_code == 200:
        data = response.json()
        return data
    elif response.status_code == 409:
        data = response.json()
        print(data['message'])
        return None

# create_default_policy("beta", 410)

def main():

    parser = argparse.ArgumentParser(description='Arguments')

    parser.add_argument('--subscription_id', required=True, help='Azure Subscription ID')
    parser.add_argument('--brand_name', required=True, help='Brand Name')
    parser.add_argument('--url', required=True, help='Brand URL')
    parser.add_argument('--bucket_name', required=True, help='AWS Bucket Name')
    parser.add_argument('--env', required=True, help='Environment')
    parser.add_argument('--t_account', required=True, help='Twilio Account ID')
    parser.add_argument('--t_token', required=True, help='Twilio Token')
    parser.add_argument('--start_number', required=True, help='Calling Number')
    parser.add_argument('--record_number', required=True, help='Recording Number')
    parser.add_argument('--user_email', required=True, help='Super Admin Email')

    args = parser.parse_args()

    env = args.env
    # brand_name = "T-Mobile"  # As per table
    user_email = args.user_email

    subscription_id = args.subscription_id
    brand_name = args.brand_name # DB/UI
    url = args.url
    url_on_env = get_url_on_env(env, url)
    bucket_name = args.bucket_name
    bucket = bucket_name if env == "prod" or env == "beta" else "caslon"

    twilio_account = args.t_account
    twilio_token = args.t_token
    start_number = f"+1{args.start_number}"
    recorded_number = f"+1{args.record_number}"

    brand_info_json = {
        "brand_name": brand_name,
        "team_name": brand_name,
        "url": url_on_env,
        "bucket": bucket
    }

    print(brand_info_json)

    azure_data_json = getResourceJSON(subscription_id)

    azure_info_json = {
        "subscription_id": subscription_id,
        "resource_group": azure_data_json["resource_group"],
        "azure_account_name": azure_data_json["luis_app"][0],
        "luis_app_subscription": azure_data_json["luis_app"][1],
        "reporting_account_name": azure_data_json["reporting_app"][0],
        "luis_reporting_subscription": azure_data_json["reporting_app"][1],
        "msspeech_key": azure_data_json["speech_services"][1],
        "speech_json": azure_data_json["speech"],
        "open_ai_json": azure_data_json["openai"],
        "luis_authoring_json": azure_data_json["luisauthoring"],
    }

    twilio_json = {
        "twilio_account": twilio_account,
        "twilio_token": twilio_token,
        "start_number": start_number,
        "recorded_number": recorded_number,
    }

    print(json.dumps(azure_info_json, indent=2))

    formatted_data_json = brand_settings_data_json(brand_info_json, azure_info_json, twilio_json)

    data_json = connect_to_rds_and_execute_email(env, "Zenarate Test", user_email)

    domain = data_json["url"]
    brand_id = data_json["brand_id"]
    password = data_json["password"]
    account_id = data_json["account_id"]
    role = data_json["role"]
    user_id = data_json["user_id"]

    domain = get_domain_on_env(env)

    access_token = fetch_access_token(domain, user_id, password)

    response_json = change_brand_settings(access_token, domain, account_id, user_id, role, formatted_data_json)

    if response_json is not None:
        brand_id = response_json["data"]["main_db_new_brand_id"]
        create_default_policy(env, brand_id)

if __name__ == "__main__":
    main()