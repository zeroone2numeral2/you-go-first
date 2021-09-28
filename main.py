import asyncio
import re
import sys
import time

from loguru import logger
import pyrogram
from pyrogram import Client
from pyrogram.raw.all import layer
from pyrogram.raw.types import UpdateUserTyping
from pyrogram.raw.types import (
    SendMessageTypingAction,
    SendMessageCancelAction,
    SendMessageChooseContactAction,
    SendMessageGamePlayAction,
    SendMessageGeoLocationAction,
    SendMessageRecordAudioAction,
    SendMessageRecordRoundAction,
    SendMessageRecordVideoAction,
    SendMessageUploadAudioAction,
    SendMessageUploadDocumentAction,
    SendMessageUploadRoundAction,
    SendMessageUploadPhotoAction,
    SendMessageUploadVideoAction
)

from config import config


class Action:
    TYPING = "typing"
    UPLOAD_PHOTO = "upload_photo"
    RECORD_VIDEO = "record_video"
    UPLOAD_VIDEO = "upload_video"
    RECORD_AUDIO = "record_audio"
    UPLOAD_AUDIO = "upload_audio"
    UPLOAD_DOCUMENT = "upload_document"
    FIND_LOCATION = "find_location"
    RECORD_VIDEO_NOTE = "record_video_note"
    UPLOAD_VIDEO_NOTE = "upload_video_note"
    PLAYING = "playing"
    CHOOSE_CONTACT = "choose_contact"
    CANCEL = "cancel"


logger.remove()
logger.add("logs/you-go-first.log", rotation="10 MB", backtrace=True, diagnose=True)
logger.add(
    sys.stdout,
    level="DEBUG",
    colorize=True,
    format="<green>{time:YYYYMMDD HH:mm:ss:SSS}</green> {level} <level>{message}</level>",
    backtrace=True,
    diagnose=True
)

app = Client(
    session_name="you-go-first-script",
    workers=1,
    **config.pyrogram
)


@app.on_raw_update()
async def on_raw_update_receive(client: Client, update, *args, **kwargs):
    if not isinstance(update, UpdateUserTyping):
        return

    words_list = re.findall(r'SendMessage([A-Z][^A-Z]*)Action', str(type(update.action)))
    action_type_str = "_".join(words_list).lower()

    if not isinstance(update.action, SendMessageCancelAction) or not config.updates.get(action_type_str, False):
        # always answer to "cancel" actions updates
        logger.info(f"'{type(update.action)}' actions are disabled")
        return
        
    if isinstance(update.action, SendMessageCancelAction):
        action = Action.CANCEL
    elif isinstance(update.action, SendMessageTypingAction):
        action = Action.TYPING
    elif isinstance(update.action, SendMessageRecordAudioAction):
        action = Action.RECORD_AUDIO
    elif isinstance(update.action, SendMessageUploadPhotoAction):
        action = Action.UPLOAD_PHOTO
    elif isinstance(update.action, SendMessageRecordVideoAction):
        action = Action.RECORD_VIDEO
    elif isinstance(update.action, SendMessageUploadVideoAction):
        action = Action.UPLOAD_VIDEO
    elif isinstance(update.action, SendMessageUploadAudioAction):
        action = Action.UPLOAD_AUDIO
    elif isinstance(update.action, SendMessageUploadDocumentAction):
        action = Action.UPLOAD_DOCUMENT
    elif isinstance(update.action, SendMessageGeoLocationAction):
        action = Action.FIND_LOCATION
    elif isinstance(update.action, SendMessageRecordRoundAction):
        action = Action.RECORD_VIDEO_NOTE
    elif isinstance(update.action, SendMessageUploadRoundAction):
        action = Action.UPLOAD_VIDEO_NOTE
    elif isinstance(update.action, SendMessageGamePlayAction):
        action = Action.PLAYING
    elif isinstance(update.action, SendMessageChooseContactAction):
        action = Action.CHOOSE_CONTACT
    else:
        logger.warning("unknown action type")
        logger.warning(update)
        return

    logger.debug(f"sending '{action}...' to {update.user_id}")
    await client.send_chat_action(update.user_id, action)


def main():
    logger.info(f'running on layer: {layer}')
    logger.info(f'pyrogram version: {pyrogram.__version__}')

    app.run()


if __name__ == '__main__':
    main()
