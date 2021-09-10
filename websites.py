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
from utils import get_chrome_driver, solve_recaptcha_v2
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

    @staticmethod
    def get_recaptcha_key(bs: BS):
        elem = bs.select_one('div.g-recaptcha')
        return elem.get('data-sitekey')


class Smm(Browser):
    URL_MAIN = 'https://smm.net'
    URL_ACCOUNT = URL_MAIN + '/account'
    HOST = 'smm.net'
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
            'Host': self.HOST,
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
    URL_ACCOUNT = URL_MAIN + 'account'
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
    URL_ACCOUNT = URL_MAIN + 'account'
    HOST = 'smmillusion.com'
    NAME = 'SmmIllusion'

    def login(self):
        session = self.session
        response = session.get(self.URL_MAIN)

        if not response.__bool__():
            raise CannotLoadPage(f'{self.__class__.__name__}: {response.reason}')

        source = response.text
        bs = BS(source, 'html.parser')
        csrf = self.get_csrf_token(bs)

        session.headers.update({'Host': self.HOST,
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
    URL_ACCOUNT = URL_MAIN + 'account'
    HOST = 'peakerr.com'
    NAME = 'PeaKerr'

    def login(self):
        session = self.session
        response = session.get(self.URL_MAIN)

        if not response.__bool__():
            raise CannotLoadPage(f'{self.__class__.__name__}: {response.reason}')

        source = response.text
        bs = BS(source, 'html.parser')
        csrf = self.get_csrf_token(bs)

        session.headers.update({'Host': self.HOST,
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


class SmmKings(Browser):
    URL_MAIN = 'https://smmkings.com/'
    URL_ACCOUNT = URL_MAIN + 'account'
    URL_SIGN_UP = URL_MAIN + 'signup'
    NAME = 'SmmKings'
    HOST = 'smmkings.com'

    def login(self):
        session = self.session
        response = session.get(self.URL_MAIN)

        if not response.__bool__():
            raise CannotLoadPage(f'{self.__class__.__name__}: {response.reason}')

        source = response.text
        bs = BS(source, 'html.parser')
        csrf = self.get_csrf_token(bs)

        captcha_key = self.get_recaptcha_key(bs)
        solved_captcha = solve_recaptcha_v2(site_key=captcha_key, site_url=self.URL_MAIN)

        if captcha_key is None:
            raise CannotFindCaptcha(self.__class__.__name__)

        session.headers.update({'Host': self.HOST,
                                'Referer': self.URL_SIGN_UP,
                                'Origin': self.URL_MAIN,
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                                              ' AppleWebKit/537.36 (KHTML, like Gecko)'
                                              ' Chrome/92.0.4515.131 YaBrowser/21.8.1.468 '
                                              'Yowser/2.5 Safari/537.36'})

        credentials = get_credentials(self.NAME)
        data = {'LoginForm[username]': credentials[0],
                'LoginForm[password]': credentials[1],
                '_csrf': csrf,
                'g-recaptcha-response': solved_captcha}

        response = session.post(self.URL_MAIN, data=data)

        name = self.get_name(session)

        if not response.__bool__() or name is None:
            raise CannotLoggedIn(f'{self.__class__.__name__}: {response.reason}')

        print('Logged in as ' + name)

        self.close()
        return name

    def get_name(self, session: Session):
        response = session.get(self.URL_MAIN)
        bs = BS(response.text, 'html.parser')
        element = bs.select_one('span.text-capitalize')
        return element.getText()


class Wiq(Browser):
    URL_MAIN = 'https://wiq.ru/'
    URL_LOGIN = URL_MAIN + 'login.php'
    URL_REQUEST = URL_MAIN + 'requests.php'
    NAME = 'Wiq'

    def login(self):
        session = self.session
        response = session.get(self.URL_LOGIN)

        if not response.__bool__():
            raise CannotLoadPage(self.__class__.__name__)

        source = response.text
        bs = BS(source, 'html.parser')
        captcha_key = self.get_recaptcha_key(bs)
        solved_captcha = solve_recaptcha_v2(site_key=captcha_key, site_url=self.URL_LOGIN)

        if captcha_key is None:
            raise CannotFindCaptcha(self.__class__.__name__)

        session.headers.update({'origin': self.URL_MAIN,
                                'referer': self.URL_LOGIN,
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                                              ' AppleWebKit/537.36 (KHTML, like Gecko)'
                                              ' Chrome/92.0.4515.131 YaBrowser/21.8.1.468 '
                                              'Yowser/2.5 Safari/537.36'})
        credentials = get_credentials(self.NAME)
        data = {'username': credentials[0],
                'password': credentials[1],
                'action': 'login',
                'g-recaptcha-response': solved_captcha}

        response = session.post(self.URL_REQUEST, data=data)
        name = self.get_name(session)

        if not response.__bool__() or name is None:
            raise CannotLoggedIn(self.__class__.__name__)

        print('Logged in as ' + name)
        self.close()
        return name

    def get_name(self, session):
        response = session.get(self.URL_MAIN)

        bs = BS(response.text, 'html.parser')
        elem = bs.select_one('a.copy-api')

        return elem.getText()[2:]


if __name__ == '__main__':
    smm = SmmKings()
    smm.login()
