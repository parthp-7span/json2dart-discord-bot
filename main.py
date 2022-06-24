import json
import discord
from discord.ext import commands
from class_generator import Generator
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
client = commands.Bot(command_prefix='/', help_command=None, intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} has Awoken!')


@client.command(name="test")
async def test(ctx):
    print('-------', ctx.channel, '---', type(ctx.channel))
    await ctx.send(f'Tested!')


# @client.event
# async def on_message(message):
#     string = message.content
#     try:
#         data = json.loads(string)
#         final_dart_code = ""
#         class_name = "DataClass"
#
#         generator = Generator(class_name, data)
#         final_dart_code += generator.create_class() + "\n\n"
#
#         for key, value in data.items():
#             if type(value) == dict:
#                 temp_generator = Generator(key.capitalize(), value)
#                 final_dart_code += temp_generator.create_class() + "\n\n"
#             elif type(value) == list:
#                 dtype = type(value[0])
#                 if dtype == dict:
#                     temp_generator = Generator(key.capitalize(), value[0])
#                     final_dart_code += temp_generator.create_class() + "\n\n"
#
#         file_name = class_name.lower() + ".dart"
#         with open(file_name, "w") as f:
#             f.write(final_dart_code)
#         await message.channel.send(file=discord.File(file_name))
#         os.remove(file_name)
#     except Exception as e:
#         print(e)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    string = message.content
    data = json.loads(string)
    class_name = "DartClass"
    file_name = "temp.dart"

    temp = []

    def checkData(d, parent):
        for k, v in d.items():
            if isinstance(v, dict):
                temp.append(parent + '-' + k)
                checkData(v, parent + '-' + k)
            elif isinstance(v, list):
                if isinstance(v[0], dict):
                    temp.append(parent + '-' + k)
                    checkData(v[0], parent + '-' + k)

    checkData(data, '')

    file = open(file_name, mode='w')

    temp_generator = Generator(class_name, data)
    file.write(temp_generator.create_class() + "\n\n")
    for i in temp:
        loc = i.split('-')
        loc.remove('')
        temp_data = data
        for k in loc:
            if isinstance(temp_data, list):
                temp_data = temp_data[0][k]
            else:
                temp_data = temp_data[k]
        if isinstance(temp_data, list):
            temp_generator = Generator(loc[-1].capitalize(), temp_data[0])
            file.write(temp_generator.create_class() + "\n\n")
        else:
            temp_generator = Generator(loc[-1].capitalize(), temp_data)
            file.write(temp_generator.create_class() + "\n\n")
    file.close()
    await message.channel.send(file=discord.File(file_name))
    os.remove(file_name)


if __name__ == "__main__":
    client.run(os.getenv('TOKEN'))
