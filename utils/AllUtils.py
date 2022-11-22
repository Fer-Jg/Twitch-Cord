# Imports for other files
from typing import TYPE_CHECKING
if TYPE_CHECKING: from bridge import MainBot

import discord
from discord.ext import commands as dcommands

from twitchio import message as tmessage
from twitchio import Channel as tChannel
from twitchio.ext import commands as tcommands

from dotmap import DotMap
from typing import Union
import datetime
import contextlib
from os import listdir
import asyncio

import unicodedata
from typing import Dict, Any, Optional
import aiohttp
import yaml


from os import getcwd
testing = getcwd().startswith("C:")

class SecretData():

    @staticmethod
    def config_data() -> Dict:
        return yaml_utils.load("configurations/text.config")

    @staticmethod
    def discord_token():
        return SecretData.config_data().get("discord_token")
    
    @staticmethod
    def twitch_token():
        return SecretData.config_data().get("twitch_token")
    
    # @staticmethod
    # def twitch_data() -> Iterable[str, str, str]:
    #     '''
    #     Returns the key, the secret and the username of the account from the config
    #     '''
    #     key = ""
    #     secret = ""
    #     username = ""
    #     return key, secret, username


class Colours():
    error = 0xff0000

class DiscordUtils():
    async def react(context : dcommands.Context, emoji : str):
        if not context.interaction: await context.message.add_reaction(emoji)
    
    async def send_webhook(ctx : dcommands.Context, content, username : str = None, avatar_url : str = None) -> None:
        async with aiohttp.ClientSession() as session:
                temp_webhook = await ctx.channel.create_webhook(name=f"{ctx.bot.user.name} webhook",
                reason="Bot webhook.")
                webhook = discord.Webhook.from_url(temp_webhook.url, adapter=discord.AsyncWebhookAdapter(session))
                if username is None:
                    username = ctx.bot.user
                if avatar_url is None:
                    avatar_url = ctx.bot.user.avatar
                await webhook.send(content, username=username, avatar_url=avatar_url)
                await temp_webhook.delete()

    async def get_reference(ctx : dcommands.Context) -> discord.Message:
        '''
        Get the reference (message which is being replayed) from a `ctx`.
        '''
        try:
            message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            return message
        except:
            await ctx.message.add_reaction("❌")
            embed = discord.Embed(title="❌ Uso del comando",
                description="Este comando se usa respondiendo a un mensaje.")
            await ctx.send(embed=embed, delete_after=5)
            return None

class my_emojis():
    bad = "❌"
    good = "✅"
    right = "➡️"
    secret = "🕵️"
    public = "🌎"
    love =  "♥"

class Text_Utils():
    emoji_dict = {' ':'▪️', 'a':'🇦', 'b':'🇧', 'c':'🇨', 'd':'🇩', 'e':'🇪', 
    'f':'🇫', 'g':'🇬', 'h':'🇭', 'i':'🇮', 'j':'🇯', 
    'k':'🇰', 'l':'🇱', 'm':'🇲', 'n':'🇳', 'o':'🇴', 
    'p':'🇵', 'q':'🇶', 'r':'🇷', 's':'🇸', 't':'🇹', 'u':'🇺', 'v':'🇻',
    'w':'🇼', 'x':'🇽', 'y':'🇾', 'z':'🇿', 
    '0': '0️⃣', '1':'1️⃣', '2':'2️⃣', '3':'3️⃣', '4':'4️⃣', '5':'5️⃣', '6':'6️⃣', '7':'7️⃣', '8':'8️⃣', '9':'9️⃣'}

    def normalize_str(string : str) -> str:
        return ''.join(c for c in unicodedata.normalize('NFD', string) if unicodedata.category(c) != 'Mn')

class yaml_utils():
    def load(load_path = str) -> Dict[str, str]:
        '''
        Loads a yaml file.
        '''
        if not testing:
            load_path = f"/config/workspace/DiscordBots/SpainMCBot/{load_path}"
        with open(load_path, 'r', encoding='utf-8') as file:
            data = yaml.load(file,Loader=yaml.FullLoader)
        return data
        
    def dump(dump_path = str, data = Dict[Any, Any]) -> None:
        '''
        Dumps data (saves data) into a yaml file.
        '''
        if not testing:
            dump_path = f"/app/{dump_path}"
        with open(dump_path, 'w', encoding='utf-8') as file:
            yaml.dump(data, dump_path)




#############################################################################################
#
#
#
#                                      EXCEPTIONS
#
#
#
#############################################################################################

class BotNotReady(dcommands.CommandError):
    def __init__(self, message: Optional[str] = None, *args: Any) -> None:
        if message: super().__init__(message, *args)
        else: super().__init__("Bot not ready for command", *args)
