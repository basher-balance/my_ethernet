import logging
import os
import pickle
import requests

from django.db import IntegrityError
from .tasks import process_user_stats
from .keys import appid
from twitch.models import Twitch_model
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope
from .managed_file import ManagedFile
from .keys import my_app_key, my_app_secret, my_id


def twitch_parse():
    logging.warning("It is time to start the dramatiq task twitch")
    Twitch_model.objects.all().delete()
    token_tw = "/home/ucsm/Документы/py/pyss/token_tw.pickle"
    refresh_token_tw = "/home/ucsm/Документы/py/pyss/refresh_token_tw.pickle"

    body = {
        "client_id": my_app_key,
        "client_secret": my_app_secret,
        "grant_type": "client_credentials",
    }

    r = requests.post("https://id.twitch.tv/oauth2/token", body)

    # data output
    keys_data = r.json()

    headers = {
        "Client-ID": my_app_key,
        "Authorization": "Bearer " + keys_data["access_token"],
    }

    twitch = Twitch(my_app_key, my_app_secret)
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
        online = twitch.get_followed_streams(my_id)
    except:
        token, refresh_token = auth.authenticate()
        with (
            ManagedFile(token_tw, "wb") as new_token,
            ManagedFile(refresh_token_tw, "wb") as new_ref_token,
        ):
            pickle.dump(token, new_token)
            pickle.dump(refresh_token, new_ref_token)
        twitch.set_user_authentication(token, target_scope, refresh_token)
        online = twitch.get_followed_streams(my_id)
    finally:
        #        streamer_lists_online = [online['data'][n]['user_login'] for n in range(len(online['data']))]
        for k in range(len(online["data"])):
            try:
                writting_streamer_in_bd = Twitch_model.objects.create(
                    streamer=online["data"][k]["user_login"]
                )
            except IntegrityError:
                pass
            else:
                writting_streamer_in_bd.save(force_update=True)
    process_user_stats.send()
