import re
import validators
from urllib.parse import urlparse


class DataCorrector:
    text: str

    def __init__(self, text):
        self.text = text

    def parse(self):
        body_text = self.text.lower()
        words = body_text.split(' ')
        for i, word in enumerate(words):
            if self.check_player_uuid(word):
                words[i] = '{player}'
            elif self.check_payment_uuid(word):
                words[i] = '{payment}'
            elif self.check_ip(word):
                words[i] = '{ip}'
            elif self.check_url(word):
                words[i] = urlparse(word).netloc + ' {url}'
            elif self.check_email(word):
                words[i] = '{email}'
            elif self.check_date(word):
                words[i] = '{date}'
            elif self.check_account_deal(word):
                words[i] = '{account/deal}'
            elif self.check_account_deal(word):
                words[i] = '{account/deal}'
            elif self.check_account(word):
                words[i] = '{account}'
        body_text = ' '.join(words)
        return body_text

    @staticmethod
    def check_player_uuid(word: str):
        return True if 'player' in word and len(word.split('-')) == 6 else False

    @staticmethod
    def check_payment_uuid(word: str):
        return True if 'payment' in word and len(word.split('-')) == 6 else False

    @staticmethod
    def check_ip(word):
        return True if re.match('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', word) is not None else False

    @staticmethod
    def check_url(word):
        return True if validators.url(word) else False

    @staticmethod
    def check_email(word):
        return True if validators.email(word) else False

    @staticmethod
    def check_date(word):
        if len(word.split('.')) == 3:
            return any(i.isdigit() for i in word.split('.'))

    @staticmethod
    def check_account_deal(word):
        return True if len(word) == 8 and all(i.isdigit() for i in word) else False

    @staticmethod
    def check_account(word):
        return True if len(word) in (6, 7) and all(i.isdigit() for i in word) else False
