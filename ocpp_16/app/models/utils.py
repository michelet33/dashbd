import json
import requests

# change the localhost to something HOST_IP on Linux or use host.docker.internal for window and mac.
# URL = os.getenv("AUTHENTICATION_SERVICE")
# LOGIN_ENDPOINT = f"{URL}/login/"
# LOGIN_ENDPOINT = "http://host.docker.internal:8080/login/"
LOGIN_ENDPOINT = "http://192.168.1.129:5000/log/add/"


async def save_log(data):
    try:
        djson = json.dumps(data)
        # the following line is responsible for suppressing the warning.
        requests.packages.urllib3.disable_warnings()
        response = requests.post(
           url=LOGIN_ENDPOINT,
           data= djson,
           timeout= 30,
           verify = False
        )

        response.raise_for_status()
    except requests.HTTPError as error:
        print(error)
