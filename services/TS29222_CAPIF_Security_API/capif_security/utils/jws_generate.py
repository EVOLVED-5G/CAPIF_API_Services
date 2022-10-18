import sys
import json
import jwt



def sign_token(claim):
    try:
        with open("/usr/src/app/capif_security/utils/server.key", "rb") as key_file:
            key_data = key_file.read()

        encoded = jwt.encode(claim, key_data, algorithm="RS256")
        return encoded

    except Exception as e:
        print("Error loading key file: %s" % str(e), file=sys.stderr)
        return e