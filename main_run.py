from utils.AllUtils import *
from bridge import *

bot = MainBot()

# will echo the provided content from *discord* to twitch
@bot.discord.command(name="twitch")
async def test_twitch(ctx : dcommands, *, content: str):
    await bot.twitch_message(message=content)
    await ctx.reply("Message sent to discord :D")

# will echo the provided content from *twitch* to discord
@tcommands.command(name="discord")
async def test_discord(ctx : tcommands, *, content: str):
    await bot.discord_message(message=content)
    await ctx.send("Message sent to twitch :D")

bot.launch()