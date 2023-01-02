from streamer_things.StreamBotUtils import *

class DiscordBot(dcommands.Bot):
    def __init__(self, bridge : 'MainBot' = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bridge = bridge
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
            dcog = "cogs_discord"
            for filename in listdir(f'./{dcog}'):
                if filename.endswith('.py'):
                    await self.load_extension(f'{dcog}.{filename[:-3]}')
                    print(f'Loaded: {filename[:-3]}')
            await self.start(SecretData.discord_token())

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
        print(f'''
        ---------------------
        | Discord Ready!
        | ID > {self.user.id}
        | Name > {self.user.name}
        | Guilds > {[guild.name for guild in self.guilds]}
        ---------------------
        ''')

    async def on_command_before_invoke(self, ctx : dcommands.Context) -> None:
        if not ctx.bot.bot_ready: raise BotNotReady

    # async def on_message(self, message):
    #     print(f"[D] {message.author.name} : {message.content}")
    #     if self.bridge: await self.bridge.twitch_message(message=message.content)
    #     await self.process_commands(message)

if __name__ == "__main__":
    bot = DiscordBot(
        command_prefix="=", 
        owner_id = 347524158181212161, 
        intents = discord.Intents.all(), 
        case_insensitive=True,
        status=discord.Status.online
        )

    bot.manual_go()
