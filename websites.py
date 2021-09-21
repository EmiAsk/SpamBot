from abc import ABC, abstractmethod

from bs4 import BeautifulSoup as BS
from requests import Session

from config import get_credentials
from exceptions import *
from utils import solve_recaptcha_v2


class Browser(ABC):
    def __init__(self):
        self.session = Session()
        self.logged_in = False

    def switch_status(self):
        self.logged_in = True

    def close(self):
        self.session.close()

    @abstractmethod
    def login(self):
        """Log in to a particular website"""

    @abstractmethod
    def create_ticket(self, theme, msg) -> dict:
        """Create ticket on a particular topic"""

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
    URL_TICKET_REQUEST = URL_MAIN + '/ticket-create'
    URL_TICKET = URL_MAIN + '/tickets'
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

        session.headers = {
            'Host': self.HOST,
            'Origin': 'https://smm.net',
            'Referer': 'https://smm.net/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                          ' AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/92.0.4515.131 YaBrowser/21.8.1.468 '
                          'Yowser/2.5 Safari/537.36'}

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

    def create_ticket(self, theme, msg):
        response = self.session.get(self.URL_TICKET)
        bs = BS(response.text, 'html.parser')
        csrf = self.get_csrf_token(bs)
        form_data = {'TicketForm[subject]': theme,
                     'TicketForm[message]': msg,
                     '_csrf': csrf}
        response = self.session.post(self.URL_TICKET_REQUEST, data=form_data)
        return response.json()


class SmmRaja(Browser):
    URL_MAIN = 'https://www.smmraja.com/'
    URL_ACCOUNT = URL_MAIN + 'account'
    URL_TICKET = URL_MAIN + 'tickets'
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

        self.switch_status()
        self.close()
        return name

    def get_name(self, session):
        response = session.get(self.URL_ACCOUNT)
        bs = BS(response.text, 'html.parser')
        elem = bs.select_one('li.nav-item.dropdown>a')

        return elem.getText().strip() if elem else None

    def create_ticket(self, theme, msg):
        response = self.session.get(self.URL_TICKET)
        bs = BS(response.text, 'html.parser')
        csrf = self.get_csrf_token(bs)
        form_data = {'subject': theme,
                     'message': msg,
                     '_csrf': csrf}
        response = self.session.post(self.URL_TICKET, data=form_data)
        return response.json()


class SmmIllusion(Browser):
    URL_MAIN = 'https://smmillusion.com/'
    URL_ACCOUNT = URL_MAIN + 'account'
    URL_TICKET = URL_MAIN + 'tickets'
    URL_TICKET_REQUEST = URL_MAIN + 'ticket-create'
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

        self.switch_status()
        self.close()
        return name

    def get_name(self, session):
        response = session.get(self.URL_ACCOUNT)
        bs = BS(response.text, 'html.parser')
        elem = bs.select_one('input[id=username]')

        return elem.get('value')

    def create_ticket(self, theme, msg):
        response = self.session.get(self.URL_TICKET)
        bs = BS(response.text, 'html.parser')
        csrf = self.get_csrf_token(bs)
        form_data = {'TicketForm[subject]': 'Other',
                     'TicketForm[message]': msg,
                     '_csrf': csrf,
                     'Transaction[ID]': '',
                     'email[ID]': '',
                     'addamount[ID]': ''
                     }
        response = self.session.post(self.URL_TICKET_REQUEST, data=form_data)

        return response.json()


class PeaKerr(Browser):
    URL_MAIN = 'https://peakerr.com/'
    URL_ACCOUNT = URL_MAIN + 'account'
    URL_TICKET_REQUEST = URL_MAIN + 'ticket-create'
    URL_TICKET = URL_MAIN + 'tickets'
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

        self.switch_status()
        self.close()
        return name

    def get_name(self, session):
        response = session.get(self.URL_ACCOUNT)
        bs = BS(response.text, 'html.parser')
        elem = bs.select_one('input[id=username]')

        return elem.get('value')

    def create_ticket(self, theme, msg):
        response = self.session.get(self.URL_TICKET)
        bs = BS(response.text, 'html.parser')
        csrf = self.get_csrf_token(bs)
        form_data = {'TicketForm[subject]': 'Other',
                     'TicketForm[message]': msg,
                     '_csrf': csrf}
        response = self.session.post(self.URL_TICKET_REQUEST, data=form_data)
        return response.json()


class SmmKings(Browser):
    URL_MAIN = 'https://smmkings.com/'
    URL_ACCOUNT = URL_MAIN + 'account'
    URL_SIGN_UP = URL_MAIN + 'signup'
    URL_TICKET_REQUEST = URL_MAIN + 'ticket-create'
    URL_TICKET = URL_MAIN + 'tickets'
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

        self.switch_status()
        self.close()
        return name

    def get_name(self, session: Session):
        response = session.get(self.URL_MAIN)
        bs = BS(response.text, 'html.parser')
        element = bs.select_one('span.text-capitalize')
        return element.getText()

    def create_ticket(self, theme, msg):
        response = self.session.get(self.URL_TICKET)
        bs = BS(response.text, 'html.parser')
        csrf = self.get_csrf_token(bs)
        form_data = {'TicketForm[subject]': 'Other',
                     'TicketForm[message]': msg,
                     '_csrf': csrf,
                     'payment-method': '',
                     'payment-code': ''}
        response = self.session.post(self.URL_TICKET_REQUEST, data=form_data)
        return response.json()


class Wiq(Browser):
    URL_MAIN = 'https://wiq.ru/'
    URL_LOGIN = URL_MAIN + 'login.php'
    URL_REQUEST = URL_MAIN + 'requests.php'
    URL_TICKET_REQUEST = URL_MAIN + 'tickets/api.php?action=createTicket'
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

        self.switch_status()
        self.close()
        return name

    def get_name(self, session):
        response = session.get(self.URL_MAIN)

        bs = BS(response.text, 'html.parser')
        elem = bs.select_one('a.copy-api')

        return elem.getText()[2:]

    def create_ticket(self, theme, msg):
        form_data = {'project_id': '1',
                     'body': msg,
                     'title': theme}
        response = self.session.post(self.URL_TICKET_REQUEST, data=form_data)

        return response.json()


class BrowserController:
    def __init__(self):
        self._websites = {}
        self.theme, self.message = '', ''
        for ws in (SmmIllusion, SmmKings, Smm, SmmRaja, Wiq, PeaKerr):
            self._websites[ws.NAME] = ws()

    def set_theme(self, theme: str):
        self.theme = theme

    def set_message(self, message: str):
        self.message = message

    def login(self, website_name):
        website = self._websites.get(website_name)
        if website is None:
            raise NameError
        return website.login()

    def create_ticket(self, website_name):
        website = self._websites.get(website_name)
        if website is None:
            raise NameError
        return website.create_ticket(theme=self.theme, msg=self.message)

    def check_if_logged_in(self, website_name):
        website = self._websites.get(website_name)
        if website is None:
            raise NameError
        return website.logged_in

    def get_websites(self):
        return tuple(self._websites.keys())


if __name__ == '__main__':
    smm = Wiq()
    smm.login()
    print(smm.create_ticket())
