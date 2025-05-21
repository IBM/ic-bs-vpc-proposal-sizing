import requests
from flask import request

import constants
from utils import PROPERTIES


class AppID:

    def is_valid_access_token(self):
        return requests.get(self._user_info_endpoint(),
                            headers=self._headers()).status_code == constants.STATUS_CODE_200

    def _headers(self):
        return {
            'Authorization': f'{request.headers.get('Authorization')}'
        }

    def _user_info_endpoint(self):
        return f'{PROPERTIES["APPID_ENDPOINT"]}/userinfo'