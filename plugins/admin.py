
# (c) @AbirHasan2005 | Modifieded By : @DC4_WARRIOR

from pyrogram import Client as Clinton
from pyrogram import filters
from config import Config
from database.access import clinton


@Clinton.on_message(filters.private & filters.command('total'))
async def sts(client, message):
    if not await clinton.is_user_login(message.from_user.id):
        await message.reply_text(text="first login to bot. /login")
        return
        
    if message.from_user.id != Config.OWNER_ID:
        await message.reply_text(text="permission denied !", quote=True)
        return

    total_users = await clinton.total_users_count()
    await message.reply_text(text=f"Total user(s) {total_users}", quote=True)
