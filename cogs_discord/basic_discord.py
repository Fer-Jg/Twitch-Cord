from utils.AllUtils import *


class General(dcommands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @dcommands.command(description="Ping your bot")
    async def ping(self, ctx):
        await ctx.send(f':ping_pong: ¡PONG!\n I am running @{round(ctx.bot.latency * 1000)}ms')

    # will echo the provided content from *discord* to twitch
    @dcommands.command(name="twitch")
    async def test_twitch(self, ctx : dcommands.Context, *, content: str):
        await self.bot.bridge.twitch_message(message=content)
        await ctx.reply("Message sent to Twitch :D")

    @dcommands.command(name="embed")
    async def emb(self, ctx):
        embed = discord.Embed()

        await ctx.send(embed=embed)
        return


async def setup(bot):
    await bot.add_cog(General(bot))