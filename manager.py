from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument
from discord.ext import commands


class Manager(commands.Cog):
    # Faz o gerenciamento do bot!

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"I'm ready! {self.bot.user.name}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send(
                "Favor enviar todos os Argumentos. Digite !help para ver os parâmetros de cada comando"
            )
        elif isinstance(error, CommandNotFound):
            await ctx.send(
                "O comando não existe. Digite +help para ver todos os comandos"
            )
        else:
            raise error


def setup(bot):
    bot.add_cog(Manager(bot))
