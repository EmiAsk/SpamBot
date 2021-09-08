from abc import ABC, abstractmethod

from bs4 import BeautifulSoup as BS
from requests import Session
# from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome, ChromeOptions
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

from exceptions import *
from utils import get_chrome_driver
from config import get_credentials


class Browser(ABC):
    def __init__(self):
        self.browser: Chrome = get_chrome_driver()
        self.session = Session()

    def close(self):
        self.session.close()

    @abstractmethod
    def login(self):
        """Log in to a particular website"""

    @staticmethod
    def get_csrf_token(bs: BS) -> str:
        elem = bs.select_one('input[name=_csrf]')
        csrf = elem.get('value')
        return csrf


class Smm(Browser):
    URL_MAIN = 'https://smm.net'
    URL_ACCOUNT = URL_MAIN + '/account'
    NAME = 'Smm'

    def login(self):
        session = self.session
        response = session.get(self.URL_MAIN)

        if not response.__bool__():
            raise CannotLoadPage(f'{self.__class__.__name__}: {response.reason}')

        source = response.text
        bs = BS(source, 'html.parser')
        csrf = self.get_csrf_token(bs)

        session.headers.update({
            'Host': 'smm.net',
            'Origin': 'https://smm.net',
            'Referer': 'https://smm.net/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                          ' AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/92.0.4515.131 YaBrowser/21.8.1.468 '
                          'Yowser/2.5 Safari/537.36'})

        credentials = get_credentials(self.NAME)
        data = {'LoginForm[username]': credentials[0],
                'LoginForm[password]': credentials[1],
                '_csrf': csrf}

        response = session.post(self.URL_MAIN, data=data)

        name = self.get_name(session)
        if not response.__bool__() or name is None:
            raise CannotLoggedIn(f'{self.__class__.__name__}: {response.reason}')

        print('Logged in as ' + name)

        self.close()
        return name

    def get_name(self, session):
        response = session.get(self.URL_ACCOUNT)
        bs = BS(response.text, 'html.parser')
        elem = bs.select_one('input[id=username]')

        return elem.get('value')


class SmmRaja(Browser):
    URL_MAIN = 'https://www.smmraja.com/'
    URL_ACCOUNT = 'https://www.smmraja.com/account'
    NAME = 'SmmRaja'

    def login(self):
        session = self.session
        response = session.get(self.URL_MAIN)

        if not response.__bool__():
            raise CannotLoadPage(f'{self.__class__.__name__}: {response.reason}')

        source = response.text
        bs = BS(source, 'html.parser')
        csrf = self.get_csrf_token(bs)

        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                          ' AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/92.0.4515.131 YaBrowser/21.8.1.468 '
                          'Yowser/2.5 Safari/537.36'})

        credentials = get_credentials(self.NAME)
        data = {'username': credentials[0],
                'password': credentials[1],
                'loginform': '1',
                '_csrf': csrf}

        response = session.post(self.URL_MAIN, data=data)

        name = self.get_name(session)
        if not response.__bool__() or name is None:
            raise CannotLoggedIn(f'{self.__class__.__name__}: {response.reason}')

        print('Logged in as ' + name)

        self.close()
        return name

    def get_name(self, session):
        response = session.get(self.URL_ACCOUNT)
        bs = BS(response.text, 'html.parser')
        elem = bs.select_one('li.nav-item.dropdown>a')

        return elem.getText().strip() if elem else None


class SmmIllusion(Browser):
    URL_MAIN = 'https://smmillusion.com/'
    URL_ACCOUNT = 'https://smmillusion.com/account'
    NAME = 'SmmIllusion'

    def login(self):
        session = self.session
        response = session.get(self.URL_MAIN)

        if not response.__bool__():
            raise CannotLoadPage(f'{self.__class__.__name__}: {response.reason}')

        source = response.text
        bs = BS(source, 'html.parser')
        csrf = self.get_csrf_token(bs)

        session.headers.update({'Host': 'smmillusion.com',
                                'Origin': self.URL_MAIN,
                                'Referer': self.URL_MAIN,
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                                              ' AppleWebKit/537.36 (KHTML, like Gecko)'
                                              ' Chrome/92.0.4515.131 YaBrowser/21.8.1.468 '
                                              'Yowser/2.5 Safari/537.36'})

        credentials = get_credentials(self.NAME)
        data = {'LoginForm[username]': credentials[0],
                'LoginForm[password]': credentials[1],
                '_csrf': csrf}

        response = session.post(self.URL_MAIN, data=data)

        name = self.get_name(session)

        if not response.__bool__() or name is None:
            raise CannotLoggedIn(f'{self.__class__.__name__}: {response.reason}')

        print('Logged in as ' + name)

        self.close()
        return name

    def get_name(self, session):
        response = session.get(self.URL_ACCOUNT)
        bs = BS(response.text, 'html.parser')
        elem = bs.select_one('input[id=username]')

        return elem.get('value')


class PeaKerr(Browser):
    URL_MAIN = 'https://peakerr.com/'
    URL_ACCOUNT = 'https://peakerr.com/account'
    NAME = 'PeaKerr'

    def login(self):
        session = self.session
        response = session.get(self.URL_MAIN)

        if not response.__bool__():
            raise CannotLoadPage(f'{self.__class__.__name__}: {response.reason}')

        source = response.text
        bs = BS(source, 'html.parser')
        csrf = self.get_csrf_token(bs)

        session.headers.update({'Host': 'peakerr.com',
                                'Origin': self.URL_MAIN,
                                'Referer': self.URL_MAIN,
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                                              ' AppleWebKit/537.36 (KHTML, like Gecko)'
                                              ' Chrome/92.0.4515.131 YaBrowser/21.8.1.468 '
                                              'Yowser/2.5 Safari/537.36'})

        credentials = get_credentials(self.NAME)
        data = {'LoginForm[username]': credentials[0],
                'LoginForm[password]': credentials[1],
                '_csrf': csrf}

        response = session.post(self.URL_MAIN, data=data)

        name = self.get_name(session)

        if not response.__bool__() or name is None:
            raise CannotLoggedIn(f'{self.__class__.__name__}: {response.reason}')

        print('Logged in as ' + name)

        self.close()
        return name

    def get_name(self, session):
        response = session.get(self.URL_ACCOUNT)
        bs = BS(response.text, 'html.parser')
        elem = bs.select_one('input[id=username]')

        return elem.get('value')


# class SmmKings(Browser):
#     URL_MAIN = 'https://smmkings.com/'
#     URL_ACCOUNT = 'https://smmkings.com/account'
#
#     def __init__(self):
#         options = ChromeOptions()
#         options.add_experimental_option('excludeSwitches', ['enable-automation'])
#         options.add_experimental_option('useAutomationExtension', False)
#         options.add_argument('--disable-blink-features=AutomationControlled')
#         options.add_argument(
#             'User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
#             '(KHTML, like Gecko) Chrome/92.0.4515.131'
#             ' YaBrowser/21.8.1.468 Yowser/2.5 Safari/537.36')
#         self.browser = Chrome()
#
#     def login(self):
#         login, password = 'Ivankov', 'Eng-6L8-b6r-rUW'
#
#         self.browser.get(self.URL_MAIN)
#         self.browser.implicitly_wait(10)
#         # elem = self.browser.find_element_by_class_name('boxed-btn')
#         # elem.click()
#         WebDriverWait(self.browser, 20).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, ".reply-button"))).click()
#
#         login_inp = self.browser.find_element_by_css_selector('input[name=LoginForm[username]]')
#         login_inp.send_keys(login)
#
#         pwd_inp = self.browser.find_element_by_css_selector('input[name=LoginForm[password]]')
#         pwd_inp.send_keys(password)
#
#         pwd_inp.send_keys(Keys.ENTER)
#
#         name = self.get_name()
#
#         if name is None:
#             raise CannotLoggedIn(self.__class__.__name__)
#
#         print('Logged in as ' + name)
#
#     def get_name(self):
#         self.browser.get(self.URL_ACCOUNT)
#         try:
#             elem = self.browser.find_element_by_css_selector('span.text-capitalize')
#             return elem.text
#         except NoSuchElementException:
#             return


# class Wiq(Browser):
#     URL_MAIN = 'https://wiq.ru/'
#     URL_LOGIN = 'https://wiq.ru/login.php'
#
#     def login(self):
#         session = self.session
#         response = session.get(self.URL_LOGIN)
#
#         if not response.__bool__():
#             raise CannotLoadPage(self.__class__.__name__)
#
#         source = response.text
#         bs = BS(source, 'html.parser')
#         captcha_key = self.get_recaptcha_key(bs)
#
#         if captcha_key is None:
#             raise CannotFindCaptcha(self.__class__.__name__)
#
#         session.headers.update({'Host': 'smmillusion.com',
#                                 'Origin': self.URL_MAIN,
#                                 'Referer': self.URL_MAIN,
#                                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
#                                               ' AppleWebKit/537.36 (KHTML, like Gecko)'
#                                               ' Chrome/92.0.4515.131 YaBrowser/21.8.1.468 '
#                                               'Yowser/2.5 Safari/537.36'})
#         data = {'LoginForm[username]': 'Ivanko',
#                 'LoginForm[password]': 'chp-JaB-94a-B7P'}
#
#         response = session.post(self.URL_MAIN, data=data)
#
#         name = self.get_name(session)
#         print(response.reason)
#         if not response.__bool__() or name is None:
#             raise CannotLoggedIn(self.__class__.__name__)
#
#         print('Logged in as ' + name)
#         return session
#
#     def get_name(self, session):
#         response = session.get(self.URL_ACCOUNT)
#         bs = BS(response.text, 'html.parser')
#         elem = bs.select_one('input[id=username]')
#
#         return elem.get('value')
#
#     @staticmethod
#     def get_recaptcha_key(bs: BS):
#         elem = bs.select('div.g-recaptcha')
#         return elem.get('data-sitekey')

