#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | Modifieded By : @DC4_WARRIOR

import logging

from pyrogram import Client as Clinton
from pyrogram import filters
from database.adduser import AddUser
from database.access import clinton
from translation import Translation
from config import Config

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


@Clinton.on_message(filters.private & filters.command(["help"]))
async def help_user(client, message):
    if not await clinton.is_user_login(message.from_user.id):
        await message.reply_text(text="first login to bot. /login")
        return

    await AddUser(client, message)
    await client.send_message(
        chat_id=message.chat.id,
        text=Translation.HELP_USER,
        disable_web_page_preview=True,
        reply_to_message_id=message.id
    )


@Clinton.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    if not await clinton.is_user_login(message.from_user.id):
        await message.reply_text(text="first login to bot. /login")
        return

    await client.send_message(
        chat_id=message.chat.id,
        text=Translation.START_TEXT.format(message.from_user.mention),
        reply_to_message_id=message.id
        )


@Clinton.on_message(filters.private & filters.command('login') & filters.reply)
async def login(client, message):
    bot_pass = message.reply_to_message.text
    if str(bot_pass) == str(Config.BOT_PASS):
        await client.send_message(
            chat_id=message.chat.id,
            text="login successfull 😍"
        )
        await clinton.set_user_login(message.from_user.id, True)
        return
    await client.send_message(
        chat_id=message.chat.id,
        text="login failed 🥺"
    )