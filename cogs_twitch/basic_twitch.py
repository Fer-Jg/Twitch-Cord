from streamer_things.StreamBotUtils import *

class General(tcommands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        pass

    @tcommands.command()
    async def ping(self, ctx: tcommands.Context):
        await ctx.send(f'PONG! {ctx.author.name}!')

    # will echo the provided content from *twitch* to discord
    @tcommands.command(name="discord")
    async def test_discord(self, ctx : tcommands.Context, *, content: str):
        await self.bot.bridge.discord_message(message=content)
        await ctx.send("Message sent to Discord :D")

def prepare(bot):
    bot.add_cog(General(bot))