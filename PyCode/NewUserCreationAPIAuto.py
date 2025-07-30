import base64
import json
from UserPackageAuto import *
from rdsConnect import *
import requests
from ProdDBAccountIdFetch import *
import argparse
# from AzureTestingJSON import *

def get_password_by_env(env):

    if env == 'prod':
        return "Prod-Zen@2025!"
    elif env == 'beta':
        return "Beta-Zen@2025!"
    elif env == 'uat':
        return "Uat-Zen@2025!"
    elif env == 'qa2':
        return "Qa2-Zen@2025!"
    elif env == 'qa':
        return "Qa-Zen@2025!"
    elif env == 'dev':
        return "Dev-Zen@2025!"

def get_user_data(first_name, last_name, email, password, tier_id_1, tier_id_2):

    user_data_json = {
        "first_name": first_name,
        "last_name": last_name,
        "preferred_name": "",
        "user_name": email,
        "email": email,
        "ui_language": "1",
        "timezone": "46",
        "hire_date": "",
        "uuid": "",
        "enable_send_credential_mail": False,
        "password": password,
        "screen_reader_support": "0",
        "status": "ACTIVE",
        "profile_url": "",
        "role_permission": [
            {
                "role_id": 1,
                "access_for": [],
                "role_name": "Admin (Admin-1 )"
            }
        ],
        "team_hierarchy": {
            "tier_1_id": tier_id_1,
            "tier_2_id": tier_id_2
        },
        "label": []
    }

    return user_data_json

def btoa_encode(user_id):
    # The string you want to encode (similar to btoa() in JavaScript)
    original_string = str(user_id)

    # Encode the string to bytes using utf-8 encoding, then Base64-encode it
    encoded_bytes = base64.b64encode(original_string.encode('utf-8'))

    # Convert the bytes back to a string
    encoded_string = encoded_bytes.decode('utf-8')

    print(encoded_string)

    return encoded_string

def create_user(access_token, domain, account_id, user_id, role, updated_data):

    url = f"https://{domain}/zen-api/idp/v2/users/create-user"

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
        print("Successfully created user.")
        return True
    return False

def fetch_access_token_team_specific(domain, original_token, access_id):

    url = f"https://{domain}/platform/auth/switched"

    # request_id = btoa_encode(user_id)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        # 'Cookie': f'_loggedIn_id={user_id};_zenarate_id={user_id};_role_id={role};Z-Request-ID={request_id};central_jwt_token={original_token};'
    }

    payload = {
        "access_id": access_id,
        "original_token": f"{original_token}"
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:

        data = response.json()

        # Fetch the access_token
        datum = data.get("data")
        access_token = datum.get("access_token")

        if access_token:
            print("Access Token:", access_token)
            return access_token
        else:
            print("Access token not found in the response.")
            return None

    else:
        print("Failed to fetch data. Status code:", response.status_code)
        print("Error message:", response.text)
        return None


def main():

    parser = argparse.ArgumentParser(description='Arguments')

    parser.add_argument('--brand_name', required=True, help='Brand Name')
    parser.add_argument('--env', required=True, help='Environment')
    parser.add_argument('--user_email', required=True, help='Super Admin Email')

    args = parser.parse_args()

    env = args.env
    brand_name = args.brand_name  # As per table
    account_list = [brand_name]
    user_email = args.user_email

    # Main Inputs
    user_first_name = "Brand"
    user_last_name = "Admin"
    new_user_password = get_password_by_env(env)
    tier_id_1, tier_id_2 = tier_ids_fetch(env, brand_name) # Need to make a function for fetching these values

    data_json = connect_to_rds_and_execute_email(env, brand_name, user_email)

    domain = data_json["url"]
    brand_id = data_json["brand_id"]
    password = data_json["password"]
    account_id = data_json["account_id"]
    role = data_json["role"]
    user_id = data_json["user_id"]

    new_user_email = f"brand.admin@{domain}"

    access_token = fetch_access_token(domain, user_id, password)

    account_ids_details = fetchAccountAccessIds(env, brand_name, user_email, account_list)

    print(account_ids_details)

    teams_token = []

    for key, val in account_ids_details.items():
        print(f"For team: {val}: ")
        team_token = fetch_access_token_team_specific(domain, access_token, val["access_id"])
        teams_token.append([val["name"], team_token])

    for data in teams_token:

        token = data[1]

        # access_token = token

        print(f"{data[0]} : {token}")

        user_data_json = get_user_data(user_first_name, user_last_name, new_user_email, new_user_password, tier_id_1, tier_id_2)

        create_user(token, domain, account_id, user_id, role, user_data_json)


if __name__ == "__main__":
    main()