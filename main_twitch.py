from utils.StreamBotUtils import *

class TwitchBot(tcommands.Bot):

    def __init__(self, bridge: 'MainBot' = None):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        self.bridge = bridge
        self.streamer = StreamerInfo()
        self.streamers = [self.streamer]
        self.channels = [x.channel for x in self.streamers]

    async def go(self):
        print("Starting Twitch bot...")
        super().__init__(token=SecretData.twitch_token(), 
                        prefix='=', 
                        initial_channels=self.channels)
        await self.start()

    async def event_ready(self):
        print(f'''----------------------------------
                \r|Logged in as | {self.nick}
                \r|User id is | {self.user_id}
                \r|Listening to: {self.channels}
                \r----------------------------------''')
    
    async def event_message(self, message : tmessage.Message):
        if message.echo: return
        print(f'''[T] {message.author.name}: {message.content}''')
        await self.handle_commands(message)

    @tcommands.command()
    async def ping(self, ctx: tcommands.Context):
        await ctx.send(f'PONG! {ctx.author.name}!')

if __name__ == "__main__":
    import asyncio
    bot = TwitchBot()
    asyncio.run(bot.go())