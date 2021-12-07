from discord.ext import commands
import random


def yes_or_no():
    return (random.choice(['sim', 'nao'])


def roll_the_dice(face):
    return random.randint(1, face)


class Talks(commands.Cog):
    #Trabalha com comandos simples!

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hello', help='te envia um olá!')
    async def send_hello(self, ctx):
        await ctx.send(f'Olá, {ctx.author.name}!')

    @commands.command(name='ping', help='te retorna pong')
    async def ping(self, ctx):
        await ctx.send('pong!')

    @commands.command(name='simounao',
                      help='responde uma pergunta de "sim ou não"')
    async def _yes_or_no(self, ctx):
        await ctx.send(f'A resposta é {yes_or_no()}')

    @commands.command(name='roleumdado', help='rola um "dado" de n lados')
    async def _roll_the_dice(self, ctx, face):
        await ctx.send(f'O dado rolou {roll_the_dice(int(face))}!')

    @commands.command(name='clear', help='limpa o chat')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount + 1)


def setup(bot):
    bot.add_cog(Talks(bot))
