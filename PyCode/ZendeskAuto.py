import requests
from labelsAccessConfigsRead import *

parser = argparse.ArgumentParser(description="Arguments")

parser.add_argument('--brand_name', required=True, help='Enter the brand name as per DB')
parser.add_argument('--env', required=True, help='Enter the Environment')

args = parser.parse_args()

brand_name = args.brand_name
env = args.env

zendesk_user_email, zendesk_user_name, brand_admin_id, brand_id = get_variables(brand_name, env)

# Replace these with your values
email = "donotreply-enablement@zenarate.com"           # Your Zendesk login email
api_token = "KR44JYiRnExO9MK7FHWQeot9LTLyqCsodpC9tL8r"       # API token from Zendesk
subdomain = "zenarate"       # e.g., "mycompany" if your URL is mycompany.zendesk.com
new_user_email = zendesk_user_email  # Email of the new user to be created
new_user_name = zendesk_user_name             # Name of the new user

print("Zendesk User Email : ", new_user_email)
print("Zendesk User Name : ", new_user_name)

# Zendesk credentials
# auth = (f"{email}/token", api_token)
# headers = {"Content-Type": "application/json"}
# new_user_name_tag = new_user_name.replace(' ', '').lower()
# # Tags to assign to the new user
# tags_to_add = [
#     "for_learners",
#     "for_managers_and_admins",
#     "for_authors",
#     "simulator_release_notes",
#     new_user_name_tag
# ]
#
# # Step: Create new user
# create_url = f"https://{subdomain}.zendesk.com/api/v2/users.json"
# payload = {
#     "user": {
#         "name": new_user_name,
#         "email": new_user_email,
#         "verified": True,  # Optional: set to True if you want the email to be marked as verified
#         "tags": tags_to_add
#     }
# }
#
# response = requests.post(create_url, json=payload, auth=auth, headers=headers)
#
# if response.status_code == 201:
#     user = response.json()['user']
#     print(f"User created successfully. ID: {user['id']}")
# else:
#     print("Failed to create user:", response.text)
