#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import os
import requests
import time

from helper_funcs.display_progress import humanbytes

def DetectFileSize(url):
    r = requests.get(url, allow_redirects=True, stream=True)
    return int(r.headers.get("content-length", 0))


def DownLoadFile(url, file_name, chunk_size, client, ud_type, message_id, chat_id):
    if os.path.exists(file_name):
        os.remove(file_name)
    if not url:
        return file_name
    r = requests.get(url, allow_redirects=True, stream=True)
    # https://stackoverflow.com/a/47342052/4723940
    total_size = int(r.headers.get("content-length", 0))
    downloaded_size = 0
    with open(file_name, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:
                fd.write(chunk)
                downloaded_size += chunk_size
            if (client is not None and ((total_size // downloaded_size) % 5) == 0 ):
                time.sleep(0.3)
                try:
                    text = "{}: {} of {}".format( ud_type, humanbytes(downloaded_size), humanbytes(total_size) )
                    client.edit_message_text(chat_id, message_id, text=text)
                except:
                    pass
    return file_name
