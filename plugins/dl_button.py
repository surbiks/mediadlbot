#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | Modifieded By : @DC4_WARRIOR

import logging
import asyncio
import os
import time
import aiohttp

from datetime import datetime
from config import Config
from plugins.custom_thumbnail import *
from translation import Translation
from helper_funcs.display_progress import (TimeFormatter, humanbytes, progress_for_pyrogram)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


async def ddl_call_back(client, callback_query):
    logger.info(callback_query)
    cb_data = callback_query.data
    # youtube_dl extractors
    tg_send_type, youtube_dl_format, youtube_dl_ext = cb_data.split("=")
    thumb_image_path = Config.DOWNLOAD_LOCATION + \
        "/" + str(callback_query.from_user.id) + ".jpg"
    youtube_dl_url = callback_query.message.reply_to_message.text
    custom_file_name = os.path.basename(youtube_dl_url)
    if "|" in youtube_dl_url:
        url_parts = youtube_dl_url.split("|")
        if len(url_parts) == 2:
            youtube_dl_url = url_parts[0]
            custom_file_name = url_parts[1]
        else:
            for entity in callback_query.message.reply_to_message.entities:
                if entity.type == "text_link":
                    youtube_dl_url = entity.url
                elif entity.type == "url":
                    o = entity.offset
                    l = entity.length
                    youtube_dl_url = youtube_dl_url[o:o + l]
        if youtube_dl_url is not None:
            youtube_dl_url = youtube_dl_url.strip()
        if custom_file_name is not None:
            custom_file_name = custom_file_name.strip()
        # https://stackoverflow.com/a/761825/4723940
        logger.info(youtube_dl_url)
        logger.info(custom_file_name)
    else:
        for entity in callback_query.message.reply_to_message.entities:
            if entity.type == "text_link":
                youtube_dl_url = entity.url
            elif entity.type == "url":
                o = entity.offset
                l = entity.length
                youtube_dl_url = youtube_dl_url[o:o + l]
    user = await client.get_me()
    mention = user.mention()
    description = Translation.CUSTOM_CAPTION_UL_FILE.format(mention)
    start = datetime.now()
    await client.edit_message_text(
        text=Translation.DOWNLOAD_START,
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.id
    )
    tmp_directory_for_each_user = Config.DOWNLOAD_LOCATION + \
        "/" + str(callback_query.from_user.id)
    if not os.path.isdir(tmp_directory_for_each_user):
        os.makedirs(tmp_directory_for_each_user)
    download_directory = tmp_directory_for_each_user + "/" + custom_file_name
    command_to_exec = []
    async with aiohttp.ClientSession() as session:
        c_time = time.time()
        try:
            await download_coroutine(
                client,
                session,
                youtube_dl_url,
                download_directory,
                callback_query.message.chat.id,
                callback_query.message.id,
                c_time
            )
        except asyncio.TimeOutError:
            await client.edit_message_text(
                text=Translation.SLOW_URL_DECED,
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.id
            )
            return False
    if os.path.exists(download_directory):
        end_one = datetime.now()
        await client.edit_message_text(
            text=Translation.UPLOAD_START,
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.id
        )
        file_size = Config.TG_MAX_FILE_SIZE + 1
        try:
            file_size = os.stat(download_directory).st_size
        except FileNotFoundError as exc:
            download_directory = os.path.splitext(
                download_directory)[0] + "." + "mkv"
            # https://stackoverflow.com/a/678242/4723940
            file_size = os.stat(download_directory).st_size
        if file_size > Config.TG_MAX_FILE_SIZE:
            await client.edit_message_text(
                chat_id=callback_query.message.chat.id,
                text=Translation.RCHD_TG_API_LIMIT,
                message_id=callback_query.message.id
            )
        else:
            # ref: message from @SOURCES_CODES
            start_time = time.time()
            # try to upload file
            if tg_send_type == "audio":
                duration = await Mdata03(download_directory)
                thumb_image_path = await Gthumb01(client, callback_query)
                await client.send_audio(
                    chat_id=callback_query.message.chat.id,
                    audio=download_directory,
                    caption=description,
                    duration=duration,
                    thumb=thumb_image_path,
                    reply_to_message_id=callback_query.message.reply_to_message.id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        Translation.UPLOAD_START,
                        callback_query.message,
                        start_time
                    )
                )
            elif tg_send_type == "file":
                thumb_image_path = await Gthumb01(client, callback_query)
                await client.send_document(
                    chat_id=callback_query.message.chat.id,
                    document=download_directory,
                    thumb=thumb_image_path,
                    caption=description,
                    reply_to_message_id=callback_query.message.reply_to_message.id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        Translation.UPLOAD_START,
                        callback_query.message,
                        start_time
                    )
                )
            elif tg_send_type == "vm":
                width, duration = await Mdata02(download_directory)
                thumb_image_path = await Gthumb02(client, callback_query, duration, download_directory)
                await client.send_video_note(
                    chat_id=callback_query.message.chat.id,
                    video_note=download_directory,
                    duration=duration,
                    length=width,
                    thumb=thumb_image_path,
                    reply_to_message_id=callback_query.message.reply_to_message.id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        Translation.UPLOAD_START,
                        callback_query.message,
                        start_time
                    )
                )
            elif tg_send_type == "video":
                width, height, duration = await Mdata01(download_directory)
                thumb_image_path = await Gthumb02(client, callback_query, duration, download_directory)
                await client.send_video(
                    chat_id=callback_query.message.chat.id,
                    video=download_directory,
                    caption=description,
                    duration=duration,
                    width=width,
                    height=height,
                    supports_streaming=True,
                    thumb=thumb_image_path,
                    reply_to_message_id=callback_query.message.reply_to_message.id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        Translation.UPLOAD_START,
                        callback_query.message,
                        start_time
                    )
                )
            else:
                logger.info("Did this happen? :\\")
            end_two = datetime.now()
            try:
                os.remove(download_directory)
                os.remove(thumb_image_path)
            except:
                pass
            time_taken_for_download = (end_one - start).seconds
            time_taken_for_upload = (end_two - end_one).seconds
            await client.edit_message_text(
                text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS.format(
                    time_taken_for_download, time_taken_for_upload),
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.id,
                disable_web_page_preview=True
            )
    else:
        await client.edit_message_text(
            text=Translation.NO_VOID_FORMAT_FOUND.format("Incorrect Link"),
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.id,
            disable_web_page_preview=True
        )


async def download_coroutine(client, session, url, file_name, chat_id, message_id, start):
    downloaded = 0
    display_message = ""
    async with session.get(url, timeout=Config.PROCESS_MAX_TIMEOUT) as response:
        total_length = int(response.headers["Content-Length"])
        content_type = response.headers["Content-Type"]
        if "text" in content_type and total_length < 500:
            return await response.release()
        await client.edit_message_text(
            chat_id,
            message_id,
            text="Initiating Download\nURL: {}\nFile Size: {}".format(url, humanbytes(total_length)))
        with open(file_name, "wb") as f_handle:
            while True:
                chunk = await response.content.read(Config.CHUNK_SIZE)
                if not chunk:
                    break
                f_handle.write(chunk)
                downloaded += Config.CHUNK_SIZE
                now = time.time()
                diff = now - start
                if round(diff % 5.00) == 0 or downloaded == total_length:
                    percentage = downloaded * 100 / total_length
                    speed = downloaded / diff
                    elapsed_time = round(diff) * 1000
                    time_to_completion = round(
                        (total_length - downloaded) / speed) * 1000
                    estimated_total_time = elapsed_time + time_to_completion
                    try:
                        current_message = "**Download Status**\nURL: {}\nFile Size: {}\nDownloaded: {}\nETA: {}".format(
                            url,
                            humanbytes(total_length),
                            humanbytes(downloaded),
                            TimeFormatter(estimated_total_time)
                        )
                        if current_message != display_message:
                            await client.edit_message_text(
                                chat_id,
                                message_id,
                                text=current_message
                            )
                            display_message = current_message
                    except Exception as e:
                        logger.info(str(e))
        return await response.release()
