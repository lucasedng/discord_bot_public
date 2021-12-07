from twilio.rest import Client
from discord.ext import commands
from googletrans import Translator
# pip install googletrans==3.1.0a0
from decouple import config

def send_message(sender, receiver, message):
    sid = 'xxxxxxxxxxxx'
    authToken = 'xxxxxxxxxxxxxxxxxxx'

    client = Client(sid, authToken)

    message = client.messages.create(to=f'whatsapp:+55{receiver}',
                                     from_='whatsapp:+14155238886',
                                     body=f'*{sender}:* {message}')


def fix_message(message):
    sentence = ''
    for palavra in message:
        sentence += f' {palavra}'

    return sentence


class Smarts(commands.Cog):
    # Comandos inteligentes!

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='calcular',
                      help='calcula uma expressão matemática.')
    async def calculate_expression(self, ctx, *expression):
        expression = "".join(expression)
        response = eval(expression)

        await ctx.send(f'A resposta é: {str(response)}')

    @commands.command(name='translate', help='traduz uma frase')
    async def translate_sentence(self, ctx, dest, src, *sentence):
        await ctx.send(Translator().translate(fix_message(sentence), dest, src).text)

    @commands.command(name='whatsapp', help='envia uma mensagem no whatsapp')
    async def send_whatsapp_message(self, ctx, receiver, *message):
        lu_num = config('LU_NUMBER')
        ma_num = config('MA_NUMBER')
        if receiver in [
                'Lucas', 'lucas', 'Lu', 'lu'
        ]:
            send_message(ctx.author.name,
                         locals()[f'{receiver[0:2].lower()}_num'],
                         fix_message(message)[1:])
        else:
            send_message(ctx.author.name, receiver, fix_message(message)[1:])

        await ctx.send(f'Mensagem enviada para {receiver} com sucesso!')


def setup(bot):
    bot.add_cog(Smarts(bot))
