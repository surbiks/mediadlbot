class Translation(object):
    START_TEXT = "Hi {},\nYou can upload File|Video To Telegram with direct link, Using this bot!\n/help for more details!"
    
    FORMAT_SELECTION = "Select the desired format: <a href='{}'>file size may be approximate</a> \nIf you want to set a custom thumbnail, send the photo before or quickly after tapping one of the buttons below.\nYou can use /deletethumbnail to delete the auto-generated thumbnail."
    
    SET_CUSTOM_USERNAME_PASSWORD = "If you want to download premium videos, provide them in the following formats:\nURLs | filename | usernames | password"
    
    DOWNLOAD_START = "📥 Download ..."
    
    UPLOAD_START = "📤 Uploading ..."
    
    RCHD_TG_API_LIMIT = "Downloaded in {} seconds.\nFile Size Detected: {}\nSorry. But, I can't upload files larger than 2GB due to Telegram API limitations."
    
    AFTER_SUCCESSFUL_UPLOAD_MSG = "Thanks for using me"
    
    AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS = "Downloaded in {} seconds.\nUploaded in {} seconds."
    
    SAVED_CUSTOM_THUMB_NAIL = "Custom video / thumbnail files saved. This image will be used in the video / file."
    
    DEL_ETED_CUSTOM_THUMB_NAIL = "✅ The custom thumbnail has been removed successfully."
    
    CUSTOM_CAPTION_UL_FILE = "{}"
    
    NO_VOID_FORMAT_FOUND = "ERROR...\n<b>YouTubeDL</b> said: {}"
    
    ABOUT_MSG = "Something About Me :\n☞My Name  : All Media Downloader\n☞Language : Python3\n☞Library  : <a href='https://docs.pyrogram.org/'>Pyrogram 1.0.7</a>"
    
    HELP_USER = "Please Follow these steps!\n1. Submit the url (eg.domain / File.mp4 | New Filename.mp4).\n2. Send Image As Custom Thumbnail (Optional).\n3. Select the button.\nSVideo - Give File as video with Screenshot\nDFile - Give File (video) as file with Screenshot\nVideo - Give File as video without Screenshot\nFiles - Give Files without Screenshots\nIf the bot doesn't respond, Ask Here."
    
    REPLY_TO_MEDIA_ALBUM_TO_GEN_THUMB = "Reply to / generate custom thumbnails to media albums, to generate custom thumbnails"
    
    ERR_ONLY_TWO_MEDIA_IN_ALBUM = "Media albums can only contain two photos. Please resend the media album, then try again, or send only two photos in one album.You can use the /rename command after receiving the file to rename it with custom thumbnail support."
    
    CANCEL_STR = "Process Canceled"
    
    ZIP_UPLOADED_STR = "Uploaded {} file in {} seconds"
    
    SLOW_URL_DECED = "Gosh that seems to be a very slow URL. Since you were screwing my home, I am in no mood to download this file. Meanwhile, why don't you try this:==> https://shrtz.me/PtsVnf6 and get me a fast URL so that I can upload to Telegram, without me slowing down for other users."
