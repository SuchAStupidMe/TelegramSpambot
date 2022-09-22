# -*- coding: utf-8 -*-
import time

import config
from database import users_from_database, user_into_database, message_sent_update, check_mark
from pyrogram import Client


# Gets users from group by id
def fetch_users( chat_link):
    with Client('anon', config.api_id, config.api_hash) as client:
        chat_id = client.get_chat(chat_link).id
        for member in client.get_chat_members(chat_id):
            user_into_database(member.user.id, member.user.username)


def message_sender(message, delay=0):
    with Client('anon', config.api_id, config.api_hash) as client:
        lst = users_from_database()
        for user in lst:
            time.sleep(delay)
            try:
                if not check_mark(user[0])[0]:
                    client.send_message(user[0], message)
                    message_sent_update(user[0])
                    print('Message sent successfully')
                else:
                    pass
            except Exception as e:
                print(e)

