# You go first!

Stupidly simple Python script that will make your Telegram account appear as "_typing..._" every time you receive a "_typing..._" update from another account (or chat).

### Installation and first run

1. install the requirements with `pip install -r requirements.txt`
2. copy `config.example.toml` and rename it to `config.toml`
3. fill the `pyrogram` section of `config.toml` with the required values (get your `api_id` and `api_hash` from https://my.telegram.org/apps - see [Pyrogram's great docs](https://docs.pyrogram.org/intro/quickstart) for more information)
4. start the script with `python main.py`
5. login to your Telegram account: insert the verification code you received on your Telegram apps, and insert your 2SV password if you have one set

### Configuring which updates to answer to

There's a number of "_typing..._"-like actions that an account can perform on Telegram. The supported ones are listed in the `updates` section of `config.toml`: from there, you can configure to which of these actions your account should react. You can also configure whether to ignore updates coming from private chats or group chats.

By default, the script only answers to "_typing_", "_recording voice message_" and "_recording video message_" updates coming from private chats.

### How "typing..."-like updates work

A Telegram account will always receive "_typing..._"-like updates from accounts for which it can access the last seen time. 
For all the other users that hide their last seen time (or that have their last seen hidden because you don't share yours), your Telegram account will receive "_typing..._"-like updates only if there has been a very recent exchange of messages (be it in the private chat with the user, or in a common group), or the user marked as read one of your private messages.

This script will answer every "_typing..._"-like update your account receives by sending the same "_typing..._"-like update to the sending peer, once per received update. The "_typing..._" status [lasts on the receiver's Telegram app for 6 seconds](https://core.telegram.org/constructor/updateUserTyping), unless the action is explicitly prematurely canceled by the account that sent the request.

_This information might be incomplete, outdated, or straight-up wrong. Telegram works in misterious ways and things are often subject to changes._

### Logs

Logs are stored in the `logs` directory. By default, they keep a non-verbose log of sent requests.

### Credits

I once saw a Twitter screenshot in a Telegram channel mirroring a subreddit, explaining this concept as a Slack bot. So I thought I could make the same thing but for Telegram.