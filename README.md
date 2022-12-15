## MediaDlBot ❤️

Telegram Bot Upload Media Files|video To telegram using direct download link. (youtube, facebook, google drive, twitter, etc).

## Feature ✨

```
• Upload HTTP/HTTPS as File/Video to Telegram.

• Upload zee5, sony.live, voot and more

• Broadcast messages, check total users

• Permanent thumbnail support

• Allow authentication user with password or public use for all

• Remove depended to mongodb (use sqlite as database)
```

## Deploy 🚀

### local host
```shell
git clone https://github.com/surbiks/mediadlbot
cd mediadlbot
pip3 install -r requirements.txt
cp sample.env .env
#edit .env file and set configs
python3 bot.py
```

### docker 
```shell
git clone https://github.com/surbiks/mediadlbot
cd mediadlbot
docker build -t mediadlbot:latest .
cp sample.env .env
#edit .env file and set configs
docker run -d --name mediadlbot --restart always -v $(pwd):/opt/app/ mediadlbot:latest
```

## Issues 

   **[Submit Issues](https://github.com/surbiks/mediadlbot/issues)**


## Credits, and Thanks to 

- [@SpEcHlDe](https://t.me/ThankTelegram) for his [AnyDLBot](https://telegram.dog/AnyDLBot)
- [Dan Tès](https://t.me/haskell) for his [Pyrogram Library](https://github.com/pyrogram/pyrogram)
- [Yoily](https://t.me/YoilyL) for his [UploaditBot](https://telegram.dog/UploaditBot)
- [@AbirHasan2005](https://t.me/AbirHasan2005) for his [database.py](https://github.com/AbirHasan2005/VideoCompress/blob/main/bot/database/database.py)
- [@DC4_WARRIOR](https://t.me/Space_X_bots)
- [@xgorn](https://t.me/xgorn)
