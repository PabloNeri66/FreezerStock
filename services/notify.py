import requests


class Notify:

    def __init__(self):
        self.__base_url = 'http://127.0.0.1:8001'

    def send_outflow_event(self, data):
        requests.post(
            f'{self.__base_url}/api/v1/webohooks/outflow',
            json=data,
            timeout=5,
        )
