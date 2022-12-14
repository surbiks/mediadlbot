
# (c) @AbirHasan2005 | X-Noid

import asyncio
import datetime
import random
import string
import time
import traceback
import aiofiles
import aiofiles.os

from pyrogram import Client as Clinton
from pyrogram import filters
from pyrogram.errors import (FloodWait, InputUserDeactivated, PeerIdInvalid,UserIsBlocked)
from database.access import clinton
from config import Config


broadcast_ids = {}


async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        return 400, f"{user_id} : deactivated\n"
    except UserIsBlocked:
        return 400, f"{user_id} : blocked the bot\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : user id invalid\n"
    except Exception as e:
        return 500, f"{user_id} : {traceback.format_exc()}\n"


@Clinton.on_message(filters.private & filters.command('broadcast') & filters.reply)
async def broadcast_(client, message):
    if message.from_user.id != Config.OWNER_ID:
        return

    all_users = await clinton.get_all_users()
    broadcast_msg = message.reply_to_message

    while True:
        broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
        if not broadcast_ids.get(broadcast_id):
            break

    out = await message.reply_text(text='Broadcast initiated! You will be notified with log file when all the users are notified.')

    start_time = time.time()
    total_users = await clinton.total_users_count()
    done = 0
    failed = 0
    success = 0

    broadcast_ids[broadcast_id] = dict(
        total=total_users,
        current=done,
        failed=failed,
        success=success
    )

    async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
        async for user in all_users:

            sts, msg = await send_msg(user_id=int(user['id']), message=broadcast_msg)
            if msg is not None:
                await broadcast_log_file.write(msg)

            if sts == 200:
                success += 1
            else:
                failed += 1

            if sts == 400:
                await clinton.delete_user(user['id'])

            done += 1
            if broadcast_ids.get(broadcast_id) is None:
                break
            else:
                broadcast_ids[broadcast_id].update(dict( current=done, failed=failed, success=success))

    if broadcast_ids.get(broadcast_id):
        broadcast_ids.pop(broadcast_id)
    completed_in = datetime.timedelta(seconds=int(time.time()-start_time))

    await asyncio.sleep(3)
    await out.delete()

    if failed == 0:
        await message.reply_text(
            text=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
            quote=True)
    else:
        await message.reply_document(
            document='broadcast.txt',
            caption=f"broadcast completed in. `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
            quote=True
        )

    await aiofiles.os.remove('broadcast.txt')
