from flask import Flask


class SendStorageFileHandler:
    def get_send_file_max_age(self, name):
        return Flask.get_send_file_max_age(self, name)
