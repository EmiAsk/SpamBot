from configparser import ConfigParser
import os

from exceptions import CredentialsError

parser = ConfigParser()
parser.read(os.path.join(os.path.dirname(__file__), '.credentials'))

CAPTCHA_API_KEY = parser['api_keys']['CAPTCHA_API_KEY']
BOT_API_KEY = parser['api_keys']['BOT_API_KEY']


def get_credentials(website: str):
    try:
        return parser[website]['login'], parser[website]['password']
    except KeyError:
        raise CredentialsError
