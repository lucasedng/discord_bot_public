import json
import random
from discord.ext import commands


def in_data(event):
    with open('DataList.json', 'r+') as file:
        data = json.load(file)
    return (True if event in data else False)


def create_item_on_data(event):
    with open('DataList.json', 'r+') as file:
        data = json.load(file)
        if not in_data(event):
            data.update({f'{event}': []})
            with open('DataList.json', 'w') as file:
                print(data)
                file.write(json.dumps(data, indent=4))
                file.close()
            return True
        else:
            return False


def remove_item_from_data(event):
    with open('DataList.json', 'r+') as file:
        data = json.load(file)
        if in_data(event):
            del data[event]
            with open('DataList.json', 'w') as file:
                print(data)
                file.write(json.dumps(data, indent=4))
                file.close()
            return True
        else:
            return False


def add_item_on_event(event, item):
    with open('DataList.json', 'r+') as file:
        data = json.load(file)
        if not item in data[event]:
            data[event].append(item)
            with open('DataList.json', 'w') as file:
                print(data)
                file.write(json.dumps(data, indent=4))
                file.close()
            return True
        else:
            return False


def remove_item_from_event(event, item):
    with open('DataList.json', 'r+') as file:
        data = json.load(file)
        if item in data[event]:
            del data[event][data[event].index(item)]
            with open('DataList.json', 'w') as file:
                print(data)
                file.write(json.dumps(data, indent=4))
                file.close()
            return True
        else:
            return False


def print_all_events():
    with open('DataList.json', 'r+') as file:
        data = json.load(file)

    events_string = ''
    for (index, item) in zip(range(len(data)), data):
        if index < len(data) - 1:
            events_string += f'- {item}\n'
        else:
            events_string += f'- {item}'

    return events_string


def random_choice_on_list(event):
    data = json.load(open('DataList.json'))
    return random.choice(data[event])


def print_event(event):
    with open('DataList.json', 'r+') as file:
        data = json.load(file)
    event_string = ''
    for item in data[event]:
        if data[event].index(item) < len(data[event]) - 1:
            event_string += f'- {item} \n'
        else:
            event_string += f'- {item}'

    return event_string


def fix_message(message):
    sentence = ''
    for palavra in message:
        sentence += f' {palavra}'

    return sentence


class Lists(commands.Cog):
    #Trabalha com listas!

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='listas', help='retorna todas as listas existentes')
    async def show_all_lists(self, ctx):
        await ctx.send(f'{print_all_events()}')

    @commands.command(name='lista',
                      help='retorna todos os itens de uma lista especifica')
    async def show_all_itens(self, ctx, *event):
        ev = fix_message(event)[1:]
        if in_data(ev):
            await ctx.send(f'{print_event(ev)}')
        else:
            await ctx.send(f'A lista "{ev}" não existe no banco de dados!')

    @commands.command(name='adicionar_lista',
                      help='adiciona uma nova lista ao banco de dados')
    async def add_in_database(self, ctx, *event):
        ev = fix_message(event)[1:]
        if in_data(ev):
            await ctx.send(f'A lista "{ev}" já existe no banco de dados!')
        else:
            create_item_on_data(ev)
            await ctx.send(f'A lista "{ev}" foi criada!')

    @commands.command(name='remover_lista',
                      help='remove uma lista do banco de dados')
    async def remove_from_database(self, ctx, *event):
        ev = fix_message(event)[1:]
        if not in_data(ev):
            await ctx.send(f'A lista "{ev}" não existe no banco de dados!')
        else:
            remove_item_from_data(ev)
            await ctx.send(f'A lista "{ev}" foi deletada!')

    @commands.command(name='adicionar_item',
                      help='adiciona um item a uma lista existente')
    async def add_in_list(self, ctx, event, *item):
        it = fix_message(item)[1:]
        if add_item_on_event(event, it):
            await ctx.send(f'O item "{it}" foi adicionado a lista "{event}"!')
        else:
            await ctx.send(f'O item "{it}" já existe na lista "{event}"!')

    @commands.command(name='remover_item',
                      help='remove uma lista do banco de dados')
    async def remove_from_lista(self, ctx, event, *item):
        it = fix_message(item)[1:]
        print(it)
        if remove_item_from_event(event, it):
            await ctx.send(f'O item "{it}" foi retirado da lista "{event}"!')
        else:
            await ctx.send(f'O item "{it}" não existe na lista "{event}"!')

    @commands.command(name='sortear_item', help='sorteio o item de uma determinada lista')
    async def pick_one_item(self, ctx, event):
        await ctx.send(f'O item sorteado foi: {random_choice_on_list(event)}')


def setup(bot):
    bot.add_cog(Lists(bot))
