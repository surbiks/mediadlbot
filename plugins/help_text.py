#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | Modifieded By : @DC4_WARRIOR

import logging

from pyrogram import Client as Clinton
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.adduser import AddUser
from translation import Translation

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


@Clinton.on_message(filters.private & filters.command(["help"]))
async def help_user(client, message):
    await AddUser(client, message)
    await client.send_message(
        chat_id=message.chat.id,
        text=Translation.HELP_USER,
        disable_web_page_preview=True,
        reply_to_message_id=message.id
    )


@Clinton.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    await client.send_message(
        chat_id=message.chat.id,
        text=Translation.START_TEXT.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Comment", url="https://t.me/ansakubotchannel/1"),
                    InlineKeyboardButton("🤖 Updates", url="https://t.me/ansakubotchannel")
                ]
            ]
        ),
            reply_to_message_id=message.id
        )
