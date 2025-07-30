import boto3
import json
from botocore.exceptions import ClientError

def fetch_secret(secret_name, region_name):
    """
    Fetch a secret from AWS Secrets Manager
    :param secret_name
    :param region_name
    :return: The secret value as a dictionary.
    """

    session = boto3.Session(region_name=region_name)
    client = session.client('secretsmanager')

    try:

        response = client.get_secret_value(SecretId=secret_name)

        # Check if the secret is stored as plain text or JSON
        if "SecretString" in response:
            secret = response["SecretString"]
        else:
            # Decode binary secrets
            secret = response["SecretBinary"].decode("utf-8")

        # Convert to a dictionary if the secret is JSON
        try:
            return json.loads(secret)
        except json.JSONDecodeError:
            return secret

    except ClientError as e:
        print(f"Error fetching secret: {e}")
        return None

def get_team_secret(env):

    if env == "prod":
        secret_name_main = "zenarate/prod/db/main"
        secret_name_teams = "zenarate/prod/db/teams"
        region_name = "us-west-1"
        return fetch_secret(secret_name_teams, region_name), fetch_secret(secret_name_main, region_name)
    elif env == "beta":
        secret_name_main = "zenarate/beta/db/main"
        secret_name_teams = "zenarate/beta/db/teams"
        region_name = "us-west-1"
        return fetch_secret(secret_name_teams, region_name), fetch_secret(secret_name_main, region_name)
    elif env == "qa":
        secret_name_main = "zenarate/qa/db/main"
        secret_name_teams = "zenarate/qa/db/teams"
        region_name = "us-west-1"
        return fetch_secret(secret_name_teams, region_name), fetch_secret(secret_name_main, region_name)
    elif env == "qa2":
        secret_name_main = "zenarate/qa2/db/main"
        secret_name_teams = "zenarate/qa2/db/teams"
        region_name = "us-west-1"
        return fetch_secret(secret_name_teams, region_name), fetch_secret(secret_name_main, region_name)
    elif env == "pa":
        secret_name_pa = "zenarate/prod-ca/db/coach"
        secret_name_main = "zenarate/prod/db/teams"
        region_name_pa = "us-west-2"
        region_name_main = "us-west-1"
        return fetch_secret(secret_name_pa, region_name_pa), fetch_secret(secret_name_main, region_name_main)

def get_secret(env):

    if env == "prod":
        secret_name_main = "zenarate/prod/db/main"
        secret_name_bot = "zenarate/prod/db/bot"
        region_name = "us-west-1"
        return fetch_secret(secret_name_main, region_name), fetch_secret(secret_name_bot, region_name)
    elif env == "beta":
        secret_name_main = "zenarate/beta/db/main"
        secret_name_bot = "zenarate/beta/db/bot"
        region_name = "us-west-1"
        return fetch_secret(secret_name_main, region_name), fetch_secret(secret_name_bot, region_name)
    elif env == "qa":
        secret_name_main = "zenarate/qa/db/main"
        secret_name_bot = "zenarate/qa/db/bot"
        region_name = "us-west-1"
        return fetch_secret(secret_name_main, region_name), fetch_secret(secret_name_bot, region_name)
    elif env == "qa2":
        secret_name_main = "zenarate/qa2/db/main"
        secret_name_bot = "zenarate/qa2/db/bot"
        region_name = "us-west-1"
        return fetch_secret(secret_name_main, region_name), fetch_secret(secret_name_bot, region_name)
    elif env == "local":
        secret_name_main = "zenarate/adilocal/db/main/root"
        secret_name_bot = "zenarate/adilocal/db/bot/root"
        region_name = "us-west-1"
        return fetch_secret(secret_name_main, region_name), fetch_secret(secret_name_bot, region_name)
    elif env == "pa":
        secret_name_pa = "zenarate/prod-ca/db/coach"
        secret_name_main = "zenarate/prod/db/main"
        region_name_pa = "us-west-2"
        region_name_main = "us-west-1"
        return fetch_secret(secret_name_pa, region_name_pa), fetch_secret(secret_name_main, region_name_main)
    elif env == "pa_local":
        secret_name_pa = "zenarate/adilocal-ca/db/coach/root"
        secret_name_main = "zenarate/adilocal/db/main/root"
        region_name_pa = "us-west-2"
        region_name_main = "us-west-1"
        return fetch_secret(secret_name_pa, region_name_pa), fetch_secret(secret_name_main, region_name_main)
    elif env == "config_store":
        secret_name_conf = "zenarate/prod/db/configstore"
        secret_name_main = "zenarate/prod/db/main"
        region_name_conf = "us-west-1"
        region_name_main = "us-west-1"
        return fetch_secret(secret_name_conf, region_name_conf), fetch_secret(secret_name_main, region_name_main)
    elif env == "config_store_beta":
        secret_name_conf = "zenarate/beta/db/configstore"
        secret_name_main = "zenarate/beta/db/main"
        region_name_conf = "us-west-1"
        region_name_main = "us-west-1"
        return fetch_secret(secret_name_conf, region_name_conf), fetch_secret(secret_name_main, region_name_main)
    elif env == "config_store_local":
        secret_name_conf = "zenarate/adilocal/db/configstore/root"
        secret_name_main = "zenarate/adilocal/db/main/root"
        region_name_conf = "us-west-1"
        region_name_main = "us-west-1"
        return fetch_secret(secret_name_conf, region_name_conf), fetch_secret(secret_name_main, region_name_main)