import json 
import asyncio
import telegram 

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler

import functools 
import os 
import logging 

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

CONFIG_FILE = "config.json"

class Configuration:
    def __init__(self, api_key: str, source_groups: list[str], destination_groups: list[str], secret_token: str, webhook_url: str): 
        self.api_key = api_key 
        self.source_groups = source_groups # A list of user names.
        self.destination_groups = destination_groups # A list of chat ids.
        self.secret_token = secret_token
        self.webhook_url = webhook_url

    def __str__(self): 
        return f"Configuration(api_key='{self.api_key}', source_groups={self.source_groups}, destination_groups={self.destination_groups}, secret_token='{self.secret_token}', webhook_url='{self.webhook_url}')"
    
@functools.cache
def get_config_file() -> Configuration: 
    '''
    This function reads the configuration file `config.json`

    `config.json` is expected to be in the following format: 

    { 
        "api_key": "API-KEY-FROM-BOT-FATHER-GOES-HERE", 
        "source_groups": [
            "source group ids 1", # usernames. 
            "source group ids 2"
        ], 
        "destination_groups": [ 
            12345678910 # chat ids. 
        ]
    }

    To get the chat ids go to https://api.telegram.org/bot<token>/getUpdates.
    '''
    with open(CONFIG_FILE, 'r') as f: 
        data = f.read() 
        config = json.loads(data)
        config = Configuration(
            api_key=config['api_key'], 
            source_groups=config['source_groups'], 
            destination_groups=config['destination_groups'], 
            secret_token=config['secret_token'], 
            webhook_url=config['webhook_url']
        )
        # print(config, type(config)) 
    return config 


async def forward_handler(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    if update.message.chat.type == "private": 
        await update.message.reply_text("If you want to contribute, go to: https://github.com/noahabe/hilcoe_forwarder 👍👍")
        return 
    
    group_username = update.message.chat.username
    src_message_link = f'https://t.me/{group_username}/{update.message.message_id}'
    if group_username in get_config_file().source_groups: 
        for single_dest_group in get_config_file().destination_groups: 
            msg = await update.message.forward(single_dest_group)
            await context.bot.send_message(text=src_message_link, chat_id=single_dest_group, reply_to_message_id=msg.message_id)

async def get_id_handler(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    id = update.effective_chat.id
    await update.message.reply_text(f"ID: `{id}` (For Dev purpose only.)")

if __name__ == '__main__': 
    application = ApplicationBuilder().token(get_config_file().api_key).build() 

    message_handler = MessageHandler(filters.ALL, forward_handler)  
    id_handler = CommandHandler('id', get_id_handler)

    application.add_handler(message_handler) 
    application.add_handler(id_handler)

    PORT = int(os.environ.get('PORT', '8443'))

    application.run_webhook(
        listen='0.0.0.0', 
        port=PORT, 
        secret_token=get_config_file().secret_token, 
        webhook_url=get_config_file().webhook_url
    )

