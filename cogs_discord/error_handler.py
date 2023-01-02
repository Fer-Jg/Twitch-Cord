from types import TracebackType
import discord
import traceback
import sys
from discord.ext import commands
from utils.AllUtils import *
import asyncio


class CommandErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """
        if hasattr(ctx.command, 'on_error'): return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None: return

        ignored = () #(commands.CommandNotFound, )
        error = getattr(error, 'original', error)

        if isinstance(error, ignored): return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')
        
        elif isinstance(error, BotNotReady):
            await ctx.reply(f"El bot no está listo para usar comandos, espera unos segundos.",
            delete_after = 5)

        elif isinstance(error, commands.CommandNotFound):
            await DiscordUtils.react(ctx, my_emojis.bad)

        elif isinstance(error, commands.BadArgument):
            types = {
                "int" : "entero",
                "str" : "texto",
                "member" : "miembro"
            }
            req, arg = None, None
            if str(error).startswith("Member"):
                req = "member"
            else:
                req, arg = str(error).split('"')[1], str(error).split('"')[3]
            await ctx.reply(content=
            (f"El argumento `{arg}` requiere un valor de tipo `{types[req]}`" if
            arg and req else "Diste un tipo de argumento inválido, intenta de nuevo."))

        elif isinstance(error, commands.NotOwner):
            await ctx.reply("Solo mi creador puede usar este comando.")

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('No tienes permiso de hacer eso.')

        elif isinstance(error, commands.MissingRole):
            message = await ctx.send(f':x: {ctx.author.mention} no tienes el rol para usar este comando.')
            await asyncio.sleep(3)
            await message.delete()

        elif isinstance(error, commands.CommandOnCooldown):
            if ctx.author.id == ctx.bot.creator.id:
                await ctx.reinvoke()
                return
            else: await ctx.send(f"❌ {ctx.author.mention} no puedes hacer esto ahora, inténtalo de nuevo después de **{round(error.retry_after,2)}** segundos",delete_after=5)

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.add_reaction(f"{my_emojis.bad}")
            await ctx.send(f"{ctx.author.mention} Te faltaron uno o más argumentos en el comando.")

        elif isinstance(error, commands.NoPrivateMessage):
                await ctx.author.send(f'El comando `{ctx.command}` **no** se puede usar en mensajes privados.')

        elif isinstance(error, commands.PrivateMessageOnly):
                await ctx.author.send(f'El comando `{ctx.command}` **solo** se puede usar en mensajes privados.')

        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send('Lo siento, este comando está deshabilitado y no puede ser usado.')

        elif isinstance(error, commands.UserNotFound):
            await ctx.reply(f"Lo siento, no pude encontrar al usuario **{error.argument}**.", delete_after = 5.0)

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:   pass

        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':
                await ctx.send('I could not find that member. Please try again.')

        else:
            print("There was an error.")
            await ctx.reply(f"Hubo un error con este comando, si crees que es importante repórtalo a {ctx.bot.creator}.")
            try:
                temp_tb = "".join(traceback.format_exception(type(error),error,error.__traceback__))
                tb_dict = {"traceback" : temp_tb, "type" : type(error),
                            "author" : ctx.author, "link" : f"{ctx.message.jump_url}"}
                ctx.bot.tracebacks.append(tb_dict)
            except Exception as e:
                print(e)
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

async def setup(bot):
    await bot.add_cog(CommandErrorHandler(bot))