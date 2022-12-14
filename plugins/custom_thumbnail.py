#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | Modifieded By : @DC4_WARRIOR

import logging
import os
import random

from PIL import Image
from config import Config
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pyrogram import Client as Clinton
from database.access import clinton
from translation import Translation
from pyrogram import filters
from database.adduser import AddUser
from helper_funcs.help_Nekmo_ffmpeg import take_screen_shot


logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


@Clinton.on_message(filters.private & filters.photo)
async def save_photo(client, message):
    await AddUser(client, message)
    await clinton.set_thumbnail(message.from_user.id, thumbnail=message.photo.file_id)
    await client.send_message(chat_id=message.chat.id, text=Translation.SAVED_CUSTOM_THUMB_NAIL, reply_to_message_id=message.id)


@Clinton.on_message(filters.private & filters.command("delthumbnail"))
async def delthumbnail(client, message):
    await AddUser(client, message)
    await clinton.set_thumbnail(message.from_user.id, thumbnail=None)
    await client.send_message(chat_id=message.chat.id, text=Translation.DEL_ETED_CUSTOM_THUMB_NAIL, reply_to_message_id=message.id)


@Clinton.on_message(filters.private & filters.command("viewthumbnail") )
async def viewthumbnail(client, message):
    await AddUser(client, message)
    thumbnail = await clinton.get_thumbnail(message.from_user.id)
    if thumbnail is not None:
        await client.send_photo(
            chat_id=message.chat.id,
            photo=thumbnail,
            caption='Your current saved thumbnail 🦠',
            reply_to_message_id=message.id
        )
    else:
        await message.reply_text(text='No Thumbnail found 🤒')


async def Gthumb01(client, callback_query):
    thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(callback_query.from_user.id) + ".jpg"
    db_thumbnail = await clinton.get_thumbnail(callback_query.from_user.id)
    if db_thumbnail is not None:
        thumbnail = await client.download_media(message=db_thumbnail, file_name=thumb_image_path)
        Image.open(thumbnail).convert("RGB").save(thumbnail)
        img = Image.open(thumbnail)
        img.resize((100, 100))
        img.save(thumbnail, "JPEG")
    else:
        thumbnail = None
    return thumbnail


async def Gthumb02(client, callback_query, duration, download_directory):
    thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(callback_query.from_user.id) + ".jpg"
    db_thumbnail = await clinton.get_thumbnail(callback_query.from_user.id)
    return (
        await client.download_media(message=db_thumbnail, file_name=thumb_image_path)
        if db_thumbnail is not None
        else await take_screen_shot(download_directory, os.path.dirname(download_directory), random.randint(0, duration - 1))
    )


async def Mdata01(download_directory):
          width = 0
          height = 0
          duration = 0
          metadata = extractMetadata(createParser(download_directory))
          if metadata is not None:
              if metadata.has("duration"):
                  duration = metadata.get('duration').seconds
              if metadata.has("width"):
                  width = metadata.get("width")
              if metadata.has("height"):
                  height = metadata.get("height")
          return width, height, duration


async def Mdata02(download_directory):

          width = 0
          duration = 0
          metadata = extractMetadata(createParser(download_directory))
          if metadata is not None:
              if metadata.has("duration"):
                  duration = metadata.get('duration').seconds
              if metadata.has("width"):
                  width = metadata.get("width")
          return width, duration


async def Mdata03(download_directory):
    duration = 0
    metadata = extractMetadata(createParser(download_directory))
    if metadata is not None and metadata.has("duration"):
        duration = metadata.get('duration').seconds
    return duration
