# External libraries
from hashlib import sha1
from time import time
import base64
import json
import hmac

try:
    from urllib2 import (Request, urlopen)
except ImportError:
    from urllib.request import (Request, urlopen)

try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus


#Initializations
lines = [line.rstrip('\n') for line in open('../website-analytics/api-keys/followerwonk.txt')]
follower_wonk_access_id_str = lines[0]
follower_wonk_secret_key_str = lines[1]

#Class for access FollowerWonk API
class FollowerWonk(object):
    @staticmethod
    def social_authority(username):
        uri = 'https://api.followerwonk.com/social-authority'

        datime = int(time() + 500)

        keyBin = follower_wonk_secret_key_str.encode('UTF-8')
        messageStr = "%s\n%s" % (follower_wonk_access_id_str, datime)
        messageBin = messageStr.encode('UTF-8')

        s = hmac.new(keyBin, messageBin, sha1).digest()
        b64 = base64.b64encode(s)
        signature = quote_plus(b64)

        auth = "AccessID=%s;Timestamp=%s;Signature=%s;" % (follower_wonk_access_id_str, datime, signature)
        req = Request("%s?screen_name=%s;%s" % (uri, username, auth),headers={'User-Agent' : "Magic Browser"})
        r = urlopen(req)

        responseStr = r.read().decode("utf-8")
        response_Json = json.loads(responseStr)

        r.close()

        if '_embedded' not in response_Json:
            return -1

        return float(response_Json['_embedded'][0]['social_authority'])