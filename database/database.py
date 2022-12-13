# (c) @AbirHasan2005 | X-Noid | @DC4_WARRIOR
import peewee
from config import Config

db = peewee.SqliteDatabase(f"{Config.SESSION_NAME}.db")

class Users(peewee.Model):
    id = peewee.IntegerField(primary_key=True)
    thumbnail = peewee.CharField()
    class Meta:
        database = db

class Database:

    def __init__(self, uri, database_name):
        db.connect()
        db.create_tables([Users], safe=True)


    async def add_user(self, id):
        if not await self.is_user_exist(id):
            user = Users.create(id=id, thumbnail='')
            user.save()


    async def get_user(self, id):
        if await self.is_user_exist(id):
            user = Users.get(Users.id == id)
            return user
        return None


    async def is_user_exist(self, id):
        query = Users.select().where(Users.id == int(id))
        return len(query) > 0


    async def total_users_count(self):
        count = Users.select().count()
        return count


    async def get_all_users(self):
        users = []
        query = Users.select()
        for user in query:
            users.append(user)
        return users


    async def delete_user(self, id):
        if await self.is_user_exist(id):
            user = Users.get(Users.id == id)
            user.delete()


    async def set_thumbnail(self, id, thumbnail):
        if await self.is_user_exist(id):
            user = Users.get(Users.id == id)
            user.thumbnail = thumbnail
            user.save()


    async def get_thumbnail(self, id):
        if await self.is_user_exist(id):
            user = Users.get(Users.id == id)
            return user.thumbnail
        return None
