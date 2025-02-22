#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | Modified By > @DC4_WARRIOR


from pyrogram import Client as Clinton
from plugins.dl_button import ddl_call_back
from plugins.youtube_dl_button import youtube_dl_call_back


@Clinton.on_callback_query()
async def button(client, callback_query):
    cb_data = callback_query.data
    if "|" in cb_data:
        await youtube_dl_call_back(client, callback_query)
    elif "=" in cb_data:
        await ddl_call_back(client, callback_query)
