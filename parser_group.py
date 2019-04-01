import json
import os

from vk_api import VkApi


class Parser:

    def __init__(self, token: str, time_to_sleep: float = 0.3):
        self.__auth(token)
        self.__time_to_sleep = time_to_sleep

    def __auth(self, token: str):
        session = VkApi(token=token)
        self.api = session.get_api()

    def start_parse(self, group_id: int) -> list:
        answer = self.api.groups.getMembers(group_id=group_id, fields='sex,bdate,photo_50,city')

        total_members = answer['items']
        total_count = answer['count']

        _offset = 1000
        while _offset < total_count:
            answer = self.api.groups.getMembers(group_id=group_id, offset=_offset, fields='sex,bdate,photo_50,city')
            total_members.extend(answer['items'])

            _offset += _offset

        return total_members


def parse_vk_group(token: str, group_id: int) -> None:
    parser = Parser(token)
    result = parser.start_parse(group_id)
    save_result_to_json(result)


def save_result_to_json(data, filename='result.json'):
    with open(filename, 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    token = os.getenv('VK_TOKEN')
    group_id = 151233763
    parse_vk_group(token, group_id)
