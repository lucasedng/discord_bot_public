from discord.ext import commands
from collections import defaultdict
import discord
import datetime
import json
import os
from datetime import date
import time


def calcAge(born):
    today = date.today()
    try:
        birthday = born.replace(year=today.year)

    except ValueError:
        birthday = born.replace(year=today.year, month=born.month + 1, day=1)

    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year


def parsedate(stringdate):
    month_lst = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
    }
    year = 0
    month = 0
    day = 0
    year1, month1, day1, hour1, minute1 = time.strftime(
        "%Y,%m,%d,%H,%M").split(',')
    date = []

    for i in month_lst.keys():
        if stringdate.lower().find(i.lower()) != -1:
            month = month_lst[i]
    date.append(month)

    for i in range(1, 32):
        if stringdate[:-5].lower().find(str(i)) != -1:
            day = i
    date.append(day)

    for i in range(1000, int(year1) + 1):
        if stringdate.lower().find(str(i)) != -1:
            year = i
    date.append(year)
    return date


def birthAlert(date):
    year1, month1, day1, hour1, minute1 = time.strftime(
        "%Y,%m,%d,%H,%M").split(',')
    b = parsedate((date))
    if month1[0] == '0' and day1[0] == '0':
        if b[-2] == int(day1[-1]) and b[-3] == int(month1[-1]):
            return True
    elif month1[0] == '0':
        print('entering...')
        if b[-2] == int(day1) and b[-3] == int(month1[-1]):
            return True
    elif day1[0] == '0':
        print('entering..')
        if b[-2] == int(day1) and b[-3] == int(month1[-1]):
            return True
    return False


def dateDiffer(date, date2):
    monthD = {
        '1': 'January',
        '2': 'February',
        '3': 'March',
        '4': 'April',
        '5': 'May',
        '6': 'June',
        '7': 'July',
        '8': 'August',
        '9': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December'
    }
    month_lst = {
        'January': 31,
        'February': 28,
        'March': 31,
        'April': 30,
        'May': 31,
        'June': 30,
        'July': 31,
        'August': 31,
        'September': 30,
        'October': 31,
        'November': 30,
        'December': 31
    }
    d = parsedate(date)
    d2 = parsedate(date2)
    year = d[-1]
    year2 = d2[-1]
    month = d[-3]
    month2 = d2[-3]
    day = d[-2]
    day2 = d2[-2]
    yearDif = year - year2
    monthDif = month - month2
    dayDif = day - day2

    minu = min(month, month2)
    total = 365 * yearDif + monthDif * month_lst[monthD[str(minu)]]
    totalDays = total + dayDif
    return totalDays


datastore = defaultdict(list)
filename = 'Data.json'


class Birthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='adicionar_aniversario',
                      help='adiciona o seu aniverário ao banco de dados')
    async def mybirthday(self, ctx, *, arg):
        message = ctx.message
        Truth = True
        date = parsedate((arg))
        age = calcAge(datetime.date(date[-1], date[-3], date[-2]))
        if os.path.exists(filename):
            print('adding birthday data....')
            with open(filename, 'r') as jsonFile:
                l = (json.load(jsonFile))
            if str(message.guild.id) in l:
                for i in l[str(message.guild.id)]:
                    for j in i:
                        if str(message.author) in i:
                            print(i[str(message.author)])
                            i[str(message.author)] = {arg: age}
                            print(i)
                            Truth = False
                            break
                if Truth:
                    l[str(message.guild.id)].append(
                        {str(message.author): {
                            arg: age
                        }})
            else:
                l[str(message.guild.id)] = [{str(message.author): {arg: age}}]
            with open(filename, 'w') as f:
                json.dump(l, f, sort_keys=True, indent=4)
            await ctx.send(
                f'O aniversário de {message.author.display_name} foi adicionado ao banco de dados!'
            )
            print('stored in Json....')
        else:
            datastore[str(message.guild.id)] = [({
                str(message.author): {
                    arg: age
                }
            })]
            print("added data in dic.....")
            with open(filename, 'w') as f:
                json.dump(datastore, f, indent=4)
            await ctx.send(
                f'O aniversário de {message.author.display_name} foi adicionado ao banco de dados!'
            )
            print('exiting ready....')

    @commands.command(name='meu_nascimento',
                      help='retorna a data do seu nascimento')
    async def born(self, ctx):
        message = ctx.message
        user = message.author
        truth = False
        if os.path.exists(filename):
            with open(filename, 'r') as jsonFile:
                loading = (json.load(jsonFile))
                for j in loading[str(message.guild.id)]:
                    if str(user) in j:
                        truth = True
                        for k in j:
                            for h in j[str(k)].keys():
                                await ctx.send(f'Você nasceu em {str(h)}')
                if not truth:
                    await ctx.send(
                        'Você não está no banco de dados! Por favor, adicione o seu aniversário!'
                    )

    @commands.command(name='minha_idade', help='retorna a sua idade')
    async def meage(self, ctx):
        message = ctx.message
        birth = 0
        if os.path.exists(filename):
            with open(filename, 'r') as jsonFile:
                loading = (json.load(jsonFile))
            for j in loading[str(message.guild.id)]:
                if str(message.author) in j:
                    for k in j:
                        for h in j[str(k)].values():
                            birth = h

            await ctx.send(f'Você tem {birth} anos!')

    @commands.command(name='diferenca',
                      help='retorna, em dias, a diferença de idade de duas pessoas')
    async def length(self, ctx, arg: discord.Member):
        other = arg
        msg = ctx.message
        yourBirth = ''
        otherBirth = ''
        if os.path.exists(filename):
            with open(filename, 'r') as jsonFile:
                loading = (json.load(jsonFile))

            for j in loading[str(msg.guild.id)]:
                if str(other) in j:
                    for k in j:
                        for i in j[str(k)].keys():
                            otherBirth = i

            for j in loading[str(msg.guild.id)]:
                if str(msg.author) in j:
                    for k in j:
                        for i in j[str(k)].keys():
                            yourBirth = i
            birthDiff = dateDiffer(yourBirth, otherBirth)
            await ctx.send(f'A diferença é de {abs(birthDiff)} dias!')

    @commands.command(name='idade', help='retorna a idade de uma pessoa')
    async def age(self, ctx, *arg: discord.Member):
        msg = ctx.message
        if os.path.exists(filename):
            with open(filename, 'r') as jsonFile:
                loading = (json.load(jsonFile))

            for i in arg:
                for j in loading[str(msg.guild.id)]:
                    if str(i) in j:
                        for k in j:
                            for h in j[str(k)].values():
                                await ctx.send(f'{i.display_name} tem {str(h)} anos de idade!')


def setup(bot):
    bot.add_cog(Birthday(bot))