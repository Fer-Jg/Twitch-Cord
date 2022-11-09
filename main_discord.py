import discord
from discord.ext import commands
import datetime
import asyncio
import contextlib
from utils.AllUtils import *
from utils.StreamBotUtils import *
from os import listdir

def get_token() -> str:
    return yaml_utils.load("configurations/text.config").get("discord_token")

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = get_token()
        self.bot_ready = False
        self.creator_id = 347524158181212161
        self.creator = None
        self.tracebacks = {}

        self.invite_link = ""
        self.streamer = StreamerInfo()

    async def main(self) -> None:
        """Starts the bot properly"""
        async with self:
            self.uptime = datetime.datetime.utcnow()
            for filename in listdir('./cogs'):
                if filename.endswith('.py'):
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f'Loaded: {filename[:-3]}')
            await self.start(self.token)

    def go(self):
        with contextlib.suppress(KeyboardInterrupt):
            asyncio.run(self.main())
    
    def set_creator(self):
        self.creator = self.get_user(self.creator_id)

def intents():
    set = discord.Intents.default()
    set.members = True
    set.message_content = True
    return set

bot = Bot(
    command_prefix="=", 
    owner_id=347524158181212161, 
    intents = intents(), 
    case_insensitive=True,
    status=discord.Status.online
    )

@bot.event
async def on_ready() -> None:
    bot.set_creator()
    bot.bot_ready = True
    activity = discord.Streaming(name=bot.streamer.name,
                                platform=bot.streamer.platform,
                                details=f"con {bot.streamer.name}",
                                url=bot.streamer.link)
    await bot.change_presence(activity=activity)
    print("bot is ready")

@bot.event
async def on_disconnect() -> None:
    print("bot disconnected")

@bot.event
async def on_connect() -> None:
    print("bot connected")

@bot.before_invoke
async def on_command_before_invoke(ctx : commands.Context) -> None:
    if not ctx.bot.bot_ready: raise BotNotReady

bot.go()
