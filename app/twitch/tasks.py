import requests
import pickle
import os

from celery import shared_task
from twitch.models import Twitch_model
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope
from utils.managed_file import ManagedFile
from core.settings import BASE_DIR


@shared_task
def twitch_task():
    Twitch_model.objects.all().delete()
    token_tw = f"{BASE_DIR}/layout/token_tw.pickle"
    refresh_token_tw = f"{BASE_DIR}/layout/refresh_token_tw.pickle"
    client_id = os.environ.get("TWITCH_CLIENT_ID")
    client_secret = os.environ.get("TWITCH_CLIENT_SECRET")
    twitch_channel_id = os.environ.get("TWITCH_CHANNEL_ID")

    body = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
    }

    r = requests.post("https://id.twitch.tv/oauth2/token", body)

    # data output
    keys_data = r.json()

    headers = {
        "Client-ID": client_id,
        "Authorization": f'Bearer {keys_data.get("access_token")}',
    }

    twitch = Twitch(client_id, client_secret)
    target_scope = [AuthScope.USER_READ_FOLLOWS]
    auth = UserAuthenticator(twitch, target_scope, force_verify=False)

    try:
        with (
            ManagedFile(token_tw, "rb") as t,
            ManagedFile(refresh_token_tw, "rb") as r_t,
        ):
            print("Reading token and refresh_token")
            token = pickle.load(t)
            refresh_token = pickle.load(r_t)
        twitch.set_user_authentication(token, target_scope, refresh_token)
        online = twitch.get_followed_streams(twitch_channel_id)
    except:
        token, refresh_token = auth.authenticate()
        with (
            ManagedFile(token_tw, "wb") as new_token,
            ManagedFile(refresh_token_tw, "wb") as new_ref_token,
        ):
            pickle.dump(token, new_token)
            pickle.dump(refresh_token, new_ref_token)
        twitch.set_user_authentication(token, target_scope, refresh_token)
        online = twitch.get_followed_streams(twitch_channel_id)
    finally:
        for k in range(len(online["data"])):
            writting_streamer_in_bd, created = Twitch_model.objects.update_or_create(
                streamer=online["data"][k]["user_login"]
            )
