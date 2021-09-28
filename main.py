import asyncio

import pyrogram
from pyrogram import Client
from pyrogram.methods.messages.send_chat_action import ChatAction
from pyrogram.raw.all import layer
from pyrogram.raw.types import UpdateUserTyping, SendMessageTypingAction
from pyrogram import filters
from pyrogram.errors import FloodWait

from config import config


app = Client(
    session_name="you-go-first-script",
    **config.pyrogram
)

typing_action_update = filters.create(lambda _, __, update: update.action and isinstance(update.action, SendMessageTypingAction))


@app.on_raw_update()
async def on_typing_action(client: Client, update, *args, **kwargs):
    if isinstance(update, UpdateUserTyping):
        if update.action and isinstance(update.action, SendMessageTypingAction):
            await client.send_chat_action(update.user_id, ChatAction.TYPING)


async def main():
    await app.start()

    me = await app.get_me()

    print('running as:', me.first_name)
    print('running on layer:', layer)
    print('pyrogram version:', pyrogram.__version__)

    await pyrogram.idle()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
