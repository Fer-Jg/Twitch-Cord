from streamer_things.StreamBotUtils import *

class TwitchBot(tcommands.Bot):

    def __init__(self, bridge: 'MainBot' = None, discord_link : int = None):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        self.bridge = bridge
        self.streamer = StreamerInfo()
        self.streamers = [self.streamer]
        self.channels = [x.channel for x in self.streamers]
        self.discord_link = discord_link

    async def go(self):
        print("Starting Twitch bot...")
        super().__init__(token=SecretData.twitch_token(), 
                        prefix='=', 
                        initial_channels=self.channels)
        await self.start()
    
    def main_channel(self) -> tChannel:
        '''
        Returns the main Twitch channel configured in the bot
        '''
        return self.get_channel(self.channels[0].replace("#",""))

    async def event_ready(self):
        print(f'''----------------------------------
                \r|Logged in as | {self.nick}
                \r|User id is | {self.user_id}
                \r|Listening to: {self.channels}
                \r----------------------------------''')
    
    async def event_message(self, message : tmessage.Message):
        if message.echo: return
        print(f'''[T] {message.author.name}: {message.content}''')
        if self.bridge:
            await self.bridge.discord_message(channel=(self.bridge.d_test_channel 
            if self.bridge.d_test_channel else self.discord_link))
        await self.handle_commands(message)

    @tcommands.command()
    async def ping(self, ctx: tcommands.Context):
        await ctx.send(f'PONG! {ctx.author.name}!')

if __name__ == "__main__":
    import asyncio
    bot = TwitchBot()
    asyncio.run(bot.go())