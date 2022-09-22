# -*- coding: utf-8 -*-
import config
from GUI import app_launch


def api_id_check():
    if config.api_id is None or not  int:
        config.api_id = int(input('api id : '))
    else: pass


def api_hash_check():
    if config.api_hash is None or not str:
        config.api_hash = input('api hash : ')
    else: pass


# You also need to fill psql login in config.py
if __name__ == '__main__':
    api_id_check()
    api_hash_check()

    app_launch()
