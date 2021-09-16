from python_rucaptcha import ReCaptchaV2

from config import CAPTCHA_API_KEY
from exceptions import SolvingCaptchaError


def solve_recaptcha_v2(site_key, site_url):
    user_answer = ReCaptchaV2.ReCaptchaV2(rucaptcha_key=CAPTCHA_API_KEY).captcha_handler(site_key=site_key,
                                                                                         page_url=site_url)

    if not user_answer['error']:
        return user_answer['captchaSolve']
    elif user_answer['error']:
        # Тело ошибки, если есть
        print(user_answer['errorBody'])
        print(user_answer['errorBody'])
        raise SolvingCaptchaError