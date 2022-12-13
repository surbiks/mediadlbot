from pyrogram import Client
from pyrogram.types import Message
from database.access import clinton


async def AddUser(bot: Client, update: Message):
    if not await clinton.is_user_exist(update.from_user.id):
           await clinton.add_user(update.from_user.id)
