import discord
from discord.ext import commands
from googletrans import Translator
from datetime import datetime

from utils.AllUtils import *


# Unimportant part
class MyHelp(commands.HelpCommand):
    tr = Translator()

    def get_command_usage(self, command):
        command_desc = ""
        if not command.help:
            if command.description == "":   command_desc = "Sin descripción"
            else: command_desc = command.description
        else: command_desc = command.help
        return '**%s%s %s **➡️ %s' % (self.context.clean_prefix, command.qualified_name, command.signature, command_desc)

    async def send_bot_help(self, mapping):
        ctx = self.context
        bot = ctx.bot
        ferjgu = bot.creator
        embed = discord.Embed(title="Categorías de comandos del bot")
        embed.set_author(name=f"Por {ferjgu}", icon_url=ferjgu.avatar)
        embed.set_thumbnail(url=bot.user.avatar)
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            commands_formatted = [f"`{c.qualified_name}`" for c in filtered]
            if commands_formatted:
                cog_name = getattr(cog, "qualified_name", "Otros").replace("_"," ")
                if cog_name!= "Otros":
                    embed.add_field(name=cog_name, value=",".join(commands_formatted), inline=False)
        embed.set_footer(text=f"Llamado por {self.context.author}",icon_url=self.context.author.avatar)
        channel = self.get_destination()
        await channel.send(embed=embed)
    
   # !help <command>
    async def send_command_help(self, command):
        embed = discord.Embed(title="Comando: %s" %(command.qualified_name))
        if command.help:    desc = command.help
        elif command.description != "": desc = command.description
        else: desc = "(Sin descripción)"
        embed.add_field(name="Descripción", value = desc)
        uso = "`%s%s %s`" % (self.context.clean_prefix, command.qualified_name, command.signature.replace("_"," "))
        embed.add_field(name="Uso", value=uso)
        if command.aliases:
            embed.add_field(name="Variantes", value=", ".join(command.aliases), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)
    
   # !help <group>
    async def send_group_help(self, group):
        aliases = ", ".join([f"`{x}`" for x in group.aliases])
        if len(group.clean_params) > 0:
            if not group.help:
                if group.description == "":   command_desc = "Sin descripción"
                else: command_desc = group.description
            else: command_desc = group.help
            desc = (f"**Descripción**: \n{command_desc}"+
                    f"\n**Variantes del comando**: \n{aliases}"+
                    "\n**Subcomandos:**")
        else:
            desc = f"Variantes del comando: {aliases}"
        embed = discord.Embed(title=f"Comandos de {self.context.clean_prefix}{group.qualified_name} {group.signature}",
        description=desc)
        for command in group.commands:
            embed.add_field(name=f"{command.name} {command.signature}",value=f"`{command.help or command.description}`", inline=False)
        embed.set_footer(text='Para ver información sobre un subcomando de esta lista usa "%s%s %s <comando>"' %
        (self.context.prefix,self.context.bot.help_command.command_attrs.get("name"),group.qualified_name))
        await self.context.send(embed=embed)
    
   # !help <cog>
    async def send_cog_help(self, cog):
        embed = discord.Embed(title="Información de *%s*"%(cog.qualified_name),description=cog.description)
        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        command_signatures = [f"{self.get_command_usage(c).replace('_',' ')}" for c in filtered]
        embed.add_field(name="Comandos",value="\n".join(command_signatures), inline=True)
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_error_message(self, error):
        error_args = error.split('"')
        error = error.replace(error_args[1],"0x0x0")
        error = self.tr.translate(error,dest="es").text
        error = error.replace("0x0x0",error_args[1])
        embed = discord.Embed(title="Error", description=error, color=0xd10404)
        channel = self.get_destination()
        await channel.send(embed=embed)


class Info(commands.Cog, description="Información general del bot."):
    def __init__(self, bot):
        self.bot = bot
        help_attrs = {
            'name' : "ayuda",
            'aliases' : ["help","comandos"],
            'cooldown': commands.CooldownMapping.from_cooldown(3, 10.0, commands.BucketType.user),
            'description' : "Muestra este mensaje"
        }
        
        help_command = MyHelp(command_attrs=help_attrs)
        help_command.cog = self # Instance of Info class
        bot.help_command = help_command
    

    #Custom checks
    def in_spainmc():
        def extended_check(ctx):
            return ctx.guild.id == 868629027907313674 or ctx.message.author.id == 347524158181212161
        return commands.check(extended_check)

    @commands.command(aliases=["creador","dev","autor","author"], Hidden = False,
    description="Créditos para mi uwu (el creador del bot)")
    async def info(self, ctx):
        await DiscordUtils.react(ctx, my_emojis.love)
        bot = ctx.bot

        embed = discord.Embed(title=f"Información de {bot.user.name}",
        description=f'''
        Bot hecho por {bot.creator.mention} para [{bot.streamer.name}]({bot.streamer.link}) :)
        ''',
        color=discord.Color.blurple(),
        timestamp = datetime.utcfromtimestamp(1667812688))

        embed.set_thumbnail(url=bot.user.avatar)
        embed.set_author(name=bot.user.name, url=f"{bot.invite_link}", icon_url=bot.user.avatar)
        embed.set_footer(text = f"@{bot.creator.name}", icon_url=bot.creator.avatar)

        embed.add_field(name="👂 Comandos", value=len(bot.commands),inline=False)
        embed.add_field(name="👁️ Usuarios", value=len(bot.users),inline=False)
        embed.add_field(name="🌐 Servidores", value=len(bot.guilds),inline=False)
        embed.add_field(name="📡 Ping actual", value=f"{round(bot.latency * 1000)} ms",inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Info(bot))