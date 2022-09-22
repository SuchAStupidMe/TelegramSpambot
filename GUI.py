# -*- coding: utf-8 -*-

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5.QtGui import QPixmap
from database import users_from_database, tables_check, amount_of_sent_users, amount_of_all_users, reset_checkmarks
from telegram import fetch_users, message_sender


class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi("GUI.ui", self)
        self.fill_users_table()
        self.all_users = int
        self.sent_users = int
        self.message = str
        self.delay = 0
        self.sent_all_users()
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.pixmap = QPixmap('background.jpg')
        self.background.setPixmap(self.pixmap)
        self.show()

        # Activities
        # Start message spam
        self.message_button.clicked.connect(self.message_sending)
        # Fetch users from group
        self.get_users_button.clicked.connect(self.get_users_from_group)
        # Sets delay
        self.delay_button.clicked.connect(self.set_delay)
        # Resets checkmarks to False
        self.reset_button.clicked.connect(self.reset_checkmarks)

        self.quit_button.clicked.connect(self.close)

    # Initial filling of Table with users
    def fill_users_table(self):
        tables_check()
        self.update_users_table()
        self.console.addItem('Tables successfully initialized')

    def update_users_table(self):
        self.users_table.clear()
        self.sent_all_users()
        users = []
        row = 0
        if users_from_database() is not None:
            for user in users_from_database():
                user = dict(user_id=user[0], username=user[1], checkmark=user[2])
                users.append(user)
            self.users_table.setRowCount(len(users))
            for user in users:
                self.users_table.setItem(row, 0, QTableWidgetItem(str(user['user_id'])))
                self.users_table.setItem(row, 1, QTableWidgetItem(user['username']))
                self.users_table.setItem(row, 2, QTableWidgetItem(str(user['checkmark'])))
                row += 1

    # Message sending
    def message_sending(self):
        self.message = self.message_line.text()
        message_sender(self.message, self.delay)
        self.sent_all_users()
        self.update_users_table()

    def get_users_from_group(self):
        if self.group_line.text != '':
            chat_link = self.group_line.text()
            fetch_users(chat_link)
            self.update_users_table()
            self.console.addItem(f"Unique users from group '{chat_link}' added")

    def set_delay(self):
        if self.delay_line.text != '':
            self.delay = int(self.delay_line.text())
            self.console.addItem(f"You set delay in {self.delay} seconds")
        else:
            self.console.addItem('Delay isn`t set')

    # Shows comparison of sent messages to all users
    def sent_all_users(self):
        self.all_users = amount_of_all_users()
        self.sent_users = amount_of_sent_users()
        self.sent_all.clear()
        self.sent_all.setText(f'{self.sent_users[0]}/{self.all_users[0]}')

    def reset_checkmarks(self):
        reset_checkmarks()
        self.update_users_table()


def app_launch():
    app = QApplication([])
    window = Window()
    app.exec_()
