import requests


class Notify:

    def __init__(self):
        self.__base_url = 'https://webhook.site'

    def send_event(self, data):
        requests.post(
            f'{self.__base_url}/017b14fe-f7ae-4ada-9d91-a2afe0589956',
            json=data,
            timeout=5,
        )
