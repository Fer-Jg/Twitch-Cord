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

class DiscordBot(commands.Bot):
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

    async def go(self):
        with contextlib.suppress(KeyboardInterrupt):
            await self.main()
        
    def manual_go(self):
        with contextlib.suppress(KeyboardInterrupt):
            asyncio.run(self.main())
    
    def set_creator(self):
        self.creator = self.get_user(self.creator_id)

    async def on_disconnect(self) -> None:
        print("bot disconnected")

    async def on_connect(self) -> None:
        print("bot connected")

    async def on_ready(self) -> None:
        self.set_creator()
        self.bot_ready = True
        activity = discord.Streaming(name=self.streamer.name,
                                    platform=self.streamer.platform,
                                    details=f"con {self.streamer.name}",
                                    url=self.streamer.link)
        await self.change_presence(activity=activity)
        print("bot is ready")

    async def on_command_before_invoke(self, ctx : commands.Context) -> None:
        if not ctx.bot.bot_ready: raise BotNotReady

        

if __name__ == "__main__":
    bot = DiscordBot(
        command_prefix="=", 
        owner_id = 347524158181212161, 
        intents = discord.Intents.all(), 
        case_insensitive=True,
        status=discord.Status.online
        )

    bot.manual_go()
