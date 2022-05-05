import pickle

from twitchAPI import Twitch, AuthScope, UserAuthenticator
from pyss.twitch_api_key import my_app_key, my_app_secret, my_id

# token = refresh_token = None
token_tw = r"C:\Users\Alexey\Documents\py\pyss\token_tw.pickle"
refresh_token_tw = r"C:\Users\Alexey\Documents\py\pyss\refresh_token_tw.pickle"

twitch = Twitch(my_app_key, my_app_secret)
target_scope = [AuthScope.USER_READ_FOLLOWS]
#auth = UserAuthenticator(twitch, target_scope, force_verify=False)

with open(token_tw, "rb") as t:
    token = pickle.load(t)

with open(refresh_token_tw, "rb") as r_t:
    refresh_token = pickle.load(r_t)
# this will open your default browser and prompt you with the twitch verification website
# token, refresh_token = auth.authenticate()

# with open(token_tw, "wb") as f:
#     print("Saving token for Future Use...")
#     pickle.dump(token, f)
#
# with open(refresh_token_tw, "wb") as f:
#     print("Saving refresh_token for Future Use...")
#     pickle.dump(refresh_token, f)

# add User authentication
twitch.set_user_authentication(token, target_scope, refresh_token)
online = twitch.get_followed_streams(my_id)

