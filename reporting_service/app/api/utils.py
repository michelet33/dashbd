import os
from functools import wraps
from typing import Any, Callable
import requests
# from requests.adapters import HTTPAdapter, Retry
from fastapi import Response

# change the localhost to something HOST_IP on Linux or use host.docker.internal for window and mac.
URL = os.getenv("AUTHENTICATION_SERVICE")
LOGIN_ENDPOINT = f"{URL}/login/"
# LOGIN_ENDPOINT = "http://host.docker.internal:8080/login/"
# LOGIN_ENDPOINT = "http://0.0.0.0:8080/login/"

def auth_required(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any):
        try:
            # the following line is responsible for suppressing the warning.
            requests.packages.urllib3.disable_warnings()
            response = requests.post(
               url=LOGIN_ENDPOINT,
               timeout= 30,
               headers={
                  "Authorization": kwargs["authorization"],
               },
                verify = False
            )

            response.raise_for_status()
            return func(*args, **kwargs)
        except requests.HTTPError as error:
            return Response(
               status_code=error.response.status_code
            )

    return wrapper
