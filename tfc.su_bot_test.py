# -*- coding: utf-8 -*
'''
Created on 11 окт. 2020 г.

@author: User
'''
import time, sched, random
from random import choice
from datetime import datetime, timedelta, date
from termcolor import cprint
import _thread
import logging

import urllib.request
import json
import re
#import codecs
import sys, os
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio


from vkbot import vk_bot_config as config

# =============================================================================================

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', help_command=None, intents=intents) #инициализируем бота с префиксом '!'

# Конфигурация
# =============================================================================================
BOT_TOKEN = ''
# nick part
main_channel_id = 764106268780396574 #644905699436134400 - канал #основной или #общий
gamechat_channel_id = 764103166072717322 #542326584422563850 - канал #чат-игры

#logging.basicConfig(filename='tfc.su_bot_test.log',level=logging.INFO)



print("\n[" + str(time.strftime("%d-%m-%Y %H:%M:%S")) + "] | Script start")
# Событие входа бота в онлайн
@bot.event
async def on_ready():
    time = datetime.now()
    print(' ')
    cprint("[" + str(time.strftime("%d-%m-%Y %H:%M:%S")) + "] | Bot is online. Waiting for commands.", 'blue') #Сообщение в консоль при завершении загрузки бота
    #print(bot.user.display_name)
    print('\n------')
    logging.info("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] | Bot is online. Waiting for commands.\n")
    #channel = bot.get_channel(main_channel_id)
    #await channel.send("Я в сети! Список комманд - !help")
    #user = bot.get_user(469850108440084492)
    #await user.send("`Я родился`")





# Команда для отображения иформации о других командах
@bot.command(aliases= ['h'])
async def help(msg):
    await msg.author.send("```Main category:\n  !help  - показывает это сообщение;\n  !map   - получить ссылку на карту сервера (алиасы - m);\n  !nick  - указать свой игровой ник (алиасы - n), работает только в канале #общий;\n      Пример - nick [game_nick], где параметр [game_nick] это ваш полный игровой ник. \n      Команду !key [code] необходимо отправить в глобальный чат сервера (/g).\n  !key   - подтверждает запрос на изменение ника, работает только в глобальном\n           чате сервера (/g);\n      Пример - key [code], где [code] код полученый от бота в личном сообщении, требование \n      идентичные ники: в игре и введенный [game_nick];\n  !rate  - получить ссылки на сайты голосования за сервер;\n  !FandD - получить ссылки на сайты с мониторингом основных конкурентов сервера;```")




# Инициализация (не трогать)
# =====================================================================================
code = random.randrange(10000, 100000)
game_nick = ""
shodan_nick = ""
message_id = 1
nick_call = False
s = sched.scheduler(time.time, time.sleep)
event1 = None
delay_ended = False
nick_started = datetime.now()

pidor_last_call = datetime.date(datetime.now())
pidor_first_use = False

dup_last_call = datetime.date(datetime.now())
dup_first_use = False

goodnight_first_use = False
goodmorn_first_use = False


def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)


# таймер 3 мин после чего включить функцию flip_flop
def timer():
    global s
    global event1
    
    # s.enter(delay, priority, function)
    event1 = s.enter(3 * 60, 1, flip_flop)
    s.run()

# переключение таймера изза неактивности после выдачи кода
def flip_flop():
    global nick_call
    global delay_ended

    nick_call = False
    delay_ended = True

    time = datetime.now()
    print("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] | Previous !nick task was cancelled due to timeout.\n")
    logging.info("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] | Previous !nick task was cancelled due to timeout.\n")
    
# =====================================================================================



# принудительно выключаем программу
@bot.command()
async def halt(msg):
    if msg.author == bot.get_user(469850108440084492):
    	sys.exit()


# Тестовая команда для проверки вставленных операций
@bot.command()
async def test(msg):
    await msg.author.send("test")
    embedVar = discord.Embed(title="Title", description="Desc", color=0x00ff00)
    embedVar.set_image(url="https://pbs.twimg.com/profile_images/1311725514814521347/L2UDOARa_400x400.jpg")
    embedVar.add_field(name="Field1", value="hi", inline=False)
    embedVar.add_field(name="Field2", value="hi2", inline=False)
    await msg.channel.send(embed=embedVar)



#@bot.command(pass_context= True)
async def arguments(msg, *args): #проверка функции мульти агрументов

    global main_channel_id

    if msg.channel.id == main_channel_id:

        if not args:

            await msg.channel.send("Try using an argument. For example: !arguments yes")

        elif args[0] == "yes":

            await msg.channel.send("This is a valid argument!")

        else:

            await msg.channel.send("Not a valid argument!")






@bot.command(pass_content=True, aliases=['upd'])
async def roadmap(msg, *argts):
    args = argts
    if isinstance(msg.channel, discord.channel.DMChannel):
        with open(os.getcwd() + '/data/roadmap', 'r', encoding= 'utf-8') as t:
            upd_text = t.read().replace("\'","\"")
        upd_json = json.loads(upd_text)
        items = upd_json['items']
        
        if not args:
            await msg.author.send("Используйте аргументы: \n - ideas для отображения списка идей вне планов разработки,\n - list для отображения списка, \n - descr [num] для просмотра описания по номеру в списке, \n - add для добавления нового пункта, \n - remove [num] confirm для перемещения пункта в корзину, \n - archive для отображения списка архива, \n - archive descr [num] для просмотра описания по номеру в архиве.")
            
        elif args[0] == "ideas":
            await msg.author.send("Список идей вне планов:\n Процент бонуса в ларьках\n Множитель скорости (от брони)\n Бижутерия из золота, серебра, платины и драг камней\n Увеличить бафы у алкоголя\n Клещи для кузни, закалка после ковки\n Зельеварение на травах, цветах, ядах\n  Болезни, влияние окружения на игрока")
            
        elif args[0] == "list":
            # send road map topics
            send_text = ""
            for item in range(len(items)):
                send_text = send_text + str(item+1) + '.\t' + str(items[item]['topic']) + '\n'
            await msg.author.send("Порядок разработки обновлений:\n" + send_text)
            
        elif args[0] == "descr":
            # send topics description
            if len(args) > 1 and not args[1] == '':
                if int(args[1]) >= 1 and int(args[1]) <= len(items):
                    index = int(args[1]) - 1
                    await msg.author.send(str(index + 1) + "-й пункт\nНазвание:   " + str(items[index]['topic']) + "\nОписание:   \n" + str(items[index]['descr']))
                else:
                    await msg.author.send("Указанный индекс находиться за пределами массива.")
            elif len(args) > 0:
                await msg.author.send("Укажите номер названия в списке.")
                
        elif args[0] == "add":
            # add new roadmap topic
            if msg.author.id == 469850108440084492:
                args_text = msg.message.content
                true_args = seperArgs(args_text, '~')
                if len(true_args) > 1 and not true_args[1] == '' and not true_args[1] == ' ':
                    if len(true_args) > 2 and not true_args[2] == '' and not true_args[2] == ' ':
                        if len(true_args) > 3:
                            await msg.author.send("Слишком много агрументов.")
                        else:
                            add_topic = true_args[1]
                            add_descr = true_args[2]
                            items.append({"topic":add_topic, "descr":add_descr})
                            
                            print("Добавлено под id " + str(len(items)))
                            
                            send_text = ""
                            for item in range(len(items)):
                                send_text = send_text + str(item+1) + '.\t' + str(items[item]['topic']) + '\n'
                            await msg.author.send("**Успешно добавлено**\n\nПорядок разработки обновлений:\n" + send_text)
                            send_text = ""
                            
                            upd_text = str({"items":items}).replace("\'", "\"")
                            with open(os.getcwd() + '/data/roadmap', 'w', encoding='utf-8') as t:
                                t.write(upd_text)
                    elif len(true_args) > 1:
                        await msg.author.send("Укажите описание нового пункта после названия. !upd add ~Здесь находится название ~Здесь находится описание")
                elif len(true_args) > 0:
                    await msg.author.send("Укажите название нового пункта после add. !upd add ~Здесь находится название ~Здесь находится описание")
                    
        elif args[0] == "swap" or args[0] == "moveto":
            # move topics
            if msg.author.id == 469850108440084492:
                if len(args) > 1 and not args[1] == '':
                    if len(args) > 2 and not args[2] == '':
                        ifrom = int(args[1]) - 1
                        ito = int(args[2]) - 1
                        if ifrom > 0 or ifrom < len(items) - 1:
                            if ito > 0 or ito < len(items) - 1:
                                
                                if args[0] == 'moveto':
                                    move = True
                                else:
                                    move = False
                                
                                if move == True:
                                    buff = items[ifrom]
                                    try:
                                        items.pop(ifrom)
                                        items.insert(ito, buff)
                                    except ValueError:
                                        print("Exception...")
                                    buff = []
                                else:
                                    ito_item = items[ito]
                                    items[ito] = items[ifrom]
                                    items[ifrom] = ito_item
                                    ito_item = []
                                
                                
                                send_text = ""
                                for item in range(len(items)):
                                    send_text = send_text + str(item+1) + '.\t' + str(items[item]['topic']) + '\n'
                                await msg.author.send("**Успешно перемещено**\n\nПорядок разработки обновлений:\n" + send_text)
                                send_text = ""
                                
                                upd_text = str({"items":items}).replace("\'", "\"")
                                with open(os.getcwd() + '/data/roadmap', 'w', encoding='utf-8') as t:
                                    t.write(upd_text)
                                upd_text = ""
                            else:
                                await msg.author.send("Индекс 'куда' указан за пределами массива.")
                        else:
                            await msg.author.send("Индекс 'откуда' указан за пределами массива.")
                        
                    elif len(args) > 1:
                        await msg.author.send("Укажите индекс куда переместить.")
                elif len(args) > 0:
                    await msg.author.send("Укажите индекс который перемещать.")
                    
        elif args[0] == "remove":
            # delete topics
            if msg.author.id == 469850108440084492:
                if len(args) > 1 and not args[1] == '':
                    if len(args) > 2 and not args[2] == '' and args[2] == 'confirm':
                        if int(args[1]) >= 1 and int(args[1]) <= len(items):
                            index = int(args[1]) - 1
                            item_arch = items[index]
                            items.pop(index)
                            send_text = ""
                            for item in range(len(items)):
                                send_text = send_text + str(item+1) + '.\t' + str(items[item]['topic']) + '\n'
                            await msg.author.send("**Успешно удалено**\n\nПорядок разработки обновлений:\n" + send_text)
                            send_text = ""
                            
                            upd_text = ""
                            upd_text = str({"items":items}).replace("\'", "\"")
                            with open(os.getcwd() + '/data/roadmap', 'w', encoding='utf-8') as t:
                                t.write(upd_text)
                            upd_text = ""
                            
                            with open(os.getcwd() + '/data/rem_archive', 'r', encoding='utf-8') as t:
                                upd_text = t.read().replace("\'","\"")
                            arch_json = json.loads(upd_text)

                            arch_arr = arch_json['items']
                            arch_json = []
                            arch_arr.insert(0, item_arch)
                            item_arch = []

                            upd_text = str({"items":arch_arr}).replace("\'", "\"")
                            arch_arr = []
                            with open(os.getcwd() + '/data/rem_archive', 'w', encoding='utf-8') as t:
                                t.write(upd_text)
                            upd_text = ""
                        else:
                        	await msg.author.send("Указанный индекс находиться за пределами массива.")
                    elif len(args) > 1:
                        await msg.author.send("Укажите ключ confirm после индекса.")
                elif len(args) > 0:
                    await msg.author.send("Укажите индекс для удаления.")
                    
        elif args[0] == "archive":
            # archive topic
            if msg.author.id == 469850108440084492:
                if len(args) > 1 and not args[1] == '':  
                    if len(args) > 2 and not args[1] == '' and args[1] == 'descr':
                    # archive see descr
                        with open(os.getcwd() + '/data/upd_archive', 'r', encoding='utf-8') as t:
                            upd_text = t.read().replace("\'","\"")
                        upd_json = json.loads(upd_text)
                        arch_items = upd_json['items']
                        
                        if int(args[2]) >= 1 and int(args[2]) <= len(arch_items):
                        # archive see num
                            index = int(args[2]) - 1
                            
                            await msg.author.send(str(index + 1) + "-й пункт\nНазвание:   " + str(arch_items[index]['topic']) + "\nОписание:   \n" + str(arch_items[index]['descr']))
                            arch_items = []
                        else:
                            await msg.author.send("Укажите номер после descr.")
                            
                    elif int(args[1]) >= 1 and int(args[1]) <= len(items):
                    # archive num
                            if len(args) > 2 and not args[2] == '' and args[2] == 'confirm':
                            # archive num confirm
                                index = int(args[1]) - 1
                                item_arch = items[index]
                                items.pop(index)

                                send_text = ""
                                for item in range(len(items)):
                                    send_text = send_text + str(item+1) + '.\t' + str(items[item]['topic']) + '\n'
                                await msg.author.send("**Успешно заархивировано.**\n\nПорядок разработки обновлений:\n" + send_text)
                                send_text = ""
                                
                                upd_text = ""
                                upd_text = str({"items":items}).replace("\'", "\"")
                                with open(os.getcwd() + '/data/roadmap', 'w', encoding='utf-8') as t:
                                    t.write(upd_text)
                                upd_text = ""

                                with open(os.getcwd() + '/data/upd_archive', 'r', encoding='utf-8') as t:
                                    upd_text = t.read().replace("\'","\"")
                                arch_json = json.loads(upd_text)

                                arch_arr = arch_json['items']
                                arch_json = []
                                arch_arr.insert(0, item_arch)
                                item_arch = []

                                upd_text = str({"items":arch_arr}).replace("\'","\"")
                                arch_arr = []
                                with open(os.getcwd() + '/data/upd_archive', 'w', encoding='utf-8') as t:
                                    t.write(upd_text)
                                upd_text = ""
                            else:
                                await msg.author.send("Укажите ключ confirm после индекса.")
                    else:
                        await msg.author.send("Номер находиться за пределами массива (требования 1 <= num <= max).")
                else:
                    with open(os.getcwd() + '/data/upd_archive', 'r', encoding='utf-8') as t:
                        upd_text = t.read().replace("\'","\"")
                    upd_json = json.loads(upd_text)
                    arch_items = upd_json['items']
                         
                    send_text = ""
                    for item in range(len(arch_items)):
                        send_text = send_text + str(item+1) + '.\t' + str(arch_items[item]['topic']) + '\n'
                    await msg.author.send("Архив обновлений (выше = новее):\n" + send_text)
                    send_text = ""
                    arch_items = []
                    await msg.author.send("Укажите \" archive descr (num)\" для просмотра описания пункта архива по номеру.\nУкажите \" archive num confirm\" чтобы переместить пункт из upd в archive.")
        else:
            await msg.author.send("Неверный аргумент комманды.")





def seperArgs(arg,delimeter):
    finalArgs = []
    toAppend = ''
    index = 0
    for i in arg:
        if(i == delimeter):
            finalArgs.append(toAppend.strip())
            toAppend = ''
        else:
            toAppend += i
        if(index == len(arg) - 1):
            finalArgs.append(toAppend.strip())
            toAppend = ''
        index += 1
    return finalArgs




@bot.command(pass_content=True, aliases=['tr'])
async def translate(msg, *args):
    #if isinstance(msg.channel, discord.channel.DMChannel):
        if not args:
            await msg.channel.send("Доступные языки для перевода:\n  Русский - арранейский (!tr arrana ~текст для перевода после символа тильды)\n  Арранейский - русский (!tr russian ~текст для перевода после символа тильды)")
            
        elif len(args) > 0 and not args[0] == "":
            if args[0] == "arrana" or args[0] == "arr":
                with open(os.getcwd() + '/data/arrana_lang', 'r', encoding= 'utf-8') as t:
                    upd_text = t.read().replace("\'","\"")
                upd_json = json.loads(upd_text)
                dict_words = upd_json['words']
                
                if len(args) > 1 and not args[1] == "":
                    text_words = []
                    output_text = ""
                    
                    input_text = msg.message.content
                    arg_text = seperArgs(input_text, '~')
                    text_words = seperArgs(arg_text[1], ' ')
                    
                    is_found = False
                    text_words_index = 0
                    for word in text_words:
                        for w in dict_words:
                            if text_words[text_words_index] in w:
                                output_text = output_text + w[text_words[text_words_index]] + " "
                                is_found = True
                                break
                        if is_found == True:
                            is_found = False
                        else:
                            output_text = output_text + text_words[text_words_index] + " "
                        
                        text_words_index = text_words_index + 1
                    
                    await msg.channel.send("Перевод:\n" + output_text)
                    
            if args[0] == "russian" or args[0] == "rus":
                with open(os.getcwd() + '/data/arrana_lang', 'r', encoding= 'utf-8') as t:
                    upd_text = t.read().replace("\'","\"")
                upd_json = json.loads(upd_text)
                dict_words = upd_json['words']
                
                if len(args) > 1 and not args[1] == "":
                    text_words = []
                    output_text = ""
                    
                    input_text = msg.message.content
                    arg_text = seperArgs(input_text, '~')
                    text_words = seperArgs(arg_text[1], ' ')
                    
                    is_found = False
                    text_words_index = 0
                    for word in text_words:
                        for w in dict_words:
                            for v in w.values(): value = str(v)
                            if text_words[text_words_index]  == value:
                                for k in w.keys(): key = str(k)
                                output_text = output_text + key + " "
                                is_found = True
                                break
                        if is_found == True:
                            is_found = False
                        else:
                            output_text = output_text + text_words[text_words_index] + " "
                        
                        text_words_index = text_words_index + 1
                    
                    await msg.channel.send("Перевод:\n" + output_text)



@bot.command(pass_content=True)
async def alloy(msg, *args):
    if isinstance(msg.channel, discord.channel.DMChannel):
        with open(os.getcwd() + '/data/alloys', 'r', encoding= 'utf-8') as t:
            upd_text = t.read().replace("\'","\"")
        upd_json = json.loads(upd_text)
        alloys = upd_json['alloys']
        
        if not args:
            await msg.author.send("Укажите сплав (пример !alloy bism_br 2):\n  bism_br (висмут бронза)\n  black_br (черная бронза)\n  bronze (бронза)\n  brass (латунь)\n  rose_gold (розовое золото)\n  st_silver (стерлинговое серебро)\n  black_st (черная сталь)\n  blue_st (синяя сталь)\n  red_st (красная сталь)")
        elif len(args) > 0 and not args[0] == "":
            if len(args) > 1 and not args[1] == "":
                #try:
                    all_names = [ "bism_br", "black_br", "bronze", "brass", "rose_gold", "st_silver", "black_st", "blue_st", "red_st" ]
                    ing_names = ["Висмут Bismith", "Олово Tin", "Цинк Zinc", "Медь Copper", "Золото Gold", "Серебро Silver", "Сталь Steel", "Никель Nikel", "Чугун Pig iron"]
                    text = "Необходимо:"
                    str_alloy = str(args[0])
                    al = all_names.index(str_alloy)
                    alloy = alloys[al]
                    ingredients = alloy[str_alloy]
                    mult = int(args[1])
                    index = 0
                    count = []
                    for i in ingredients:
                        count.append(float(i)*mult)
                        if not count[index] == 0.0:
                            text = text + "\n" + ing_names[index] + " - " + str(count[index]) + " (" + str(float(i)) + "%)"
                        index = index + 1
                    ing_names = []
                    all_names = []
                    mult = 0
                    str_alloy = ""
                    al = 0
                    alloy = {}
                    ingredients = []
                    
                #except:
                    #await msg.author.send("Укажите сплав (пример !alloy bism_br 2):\n  bism_br (висмут бронза)\n  black_br (черная бронза)\n  bronze (бронза)\n  brass (латунь)\n  rose_gold (розовое золото)\n  st_silver (стерлинговое серебро)\n  black_st (черная сталь)\n  blue_st (синяя сталь)\n  red_st (красная сталь)")
                    await msg.author.send(text)
        else:
            await msg.author.send("Укажите сплав (пример !alloy bism_br):\n  bism_br (висмут бронза)\n  black_br (черная бронза)\n bronze (бронза)\n  brass (латунь)\n  rose_gold (розовое золото)\n  st_silver (стерлинговое серебро)\n  black_st (черная сталь)\n  blue_st (синяя сталь)\n  red_st (красная сталь)")





# Команда для получения ссылок на страницы рейтинга сервера
@bot.command()
async def rate(msg):
    embedVar = discord.Embed(title="", description="Ссылки на сайты рейтинга сервера", color=0x00ff00)
    embedVar.add_field(name="Основной - Minecraft Rating", value="[minecraftrating.ru](http://minecraftrating.ru/vote/2972/)", inline=False)
    embedVar.add_field(name="Top Craft", value="[topcraft.ru](https://topcraft.ru/servers/8709/)", inline=True)
    embedVar.add_field(name="MC Servera", value="[mc-servera.net](https://mc-servera.net/79302)", inline=True)
    await msg.channel.send(embed=embedVar)



# Команда для получения ссылок на основных конкурентов сервера
@bot.command()
async def FandD(msg):
    embedVar = discord.Embed(title="Ебем и Сушим (F&D)", description="Мониторинг:", color=0x00ff00)
    embedVar.add_field(name="Sky Mine (TerraFirmaCraft)", value="[sky-mine.ru](https://sky-mine.ru/about-terrafirmacraft.html)", inline=False)
    embedVar.add_field(name="Ordinary Mine (Inferno)", value="[ordinary-minecraft.ru](https://ordinary-minecraft.ru/pages/inferno-stats)", inline=True)
    embedVar.add_field(name="Hilarious (TFC)", value="[hil.su](https://hil.su/)", inline=False)
    embedVar.add_field(name="Atom Craft (Hordeum)", value="[atomcraft.ru](https://atomcraft.ru/hordeum.html)", inline=True)
    embedVar.add_field(name="Square Land (Lambda)", value="[squareland.ru](http://squareland.ru/server/lambda)", inline=False)
    embedVar.add_field(name="Grimward (DarkAges) - Выбыл (RIP)", value="[hotmc.ru](https://hotmc.ru/minecraft-server-194185)", inline=True)
    embedVar.add_field(name="Up world (Yeridan)", value="[up-world.ru](https://up-world.ru/yeridan-server-s-modom-terrafirmacraft/)", inline=False)
    await msg.channel.send(embed=embedVar)



# Команда на получение ссылки на карту сервера
@bot.command(aliases= ['m'])
async def map(msg):
    """получить ссылку на карту сервера (алиасы - m);"""
    await msg.channel.send("Карта (by xelo, SushiMan) - http://sushiweb.pp.ua/maptfc")



# Команда на изменение ника внутри группы дискорда на игровой ник
@bot.command(pass_context= True, aliases= ['n'])
async def nick(msg, *args):
    
    """указать свой игровой ник (алиасы - n);"""
    
    global main_channel_id
    if msg.channel.id == main_channel_id:
        
        global nick_call
        global message_id
        global nick_started
        
        if nick_call == False:
            
            if not args:
                
                logging.warning("\nAttempt to call !nick - no arguments")
                await msg.author.send("⛔ Укажите свой игровой ник !nick nickname.")
                
            elif len(args[0]) >= 2 and not args[0].count("@") and not args[0].count("!") and not args[0].count("#") and not args[0].count("$") and not args[0].count("%") and not args[0].count("^") and not args[0].count("&") and not args[0].count("*") and not args[0].count("(") and not args[0].count(")") and not args[0].count("-") and not args[0].count("+") and not args[0].count("=") and not args[0].count(",") and not args[0].count(".") and not args[0].count("/") and not args[0].count("?") and not args[0].count("/") and not args[0].count("\\") and not args[0].count("|") and not args[0].count("[") and not args[0].count("]") and not args[0].count("{") and not args[0].count("}") and not args[0].count("\'") and not args[0].count("\"") and not args[0].count("`") and not args[0].count("~") :
                
                global game_nick
                global code
                global delay_ended
                
                if delay_ended == True:
                    delay_ended = False
                    if isinstance(message_id, discord.Message):
                    	await message_id.add_reaction('🕒')
                
                message_id = msg.message
                game_nick = args[0]
                code = random.randrange(10000, 100000)
                
                await msg.author.send("Напишите этот ключ в глобальный чат игры - " + "!key " + str(code))
                
                time = datetime.now()
                print("\n[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] | New !nick task. Waiting for !key command. Discord username - " + message_id.author.name + ". Entered nickname - " + game_nick + ".")
                logging.info("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] | New !nick task. Waiting for !key command. Discord username - " + message_id.author.name + ". Entered nickname - " + game_nick + ".")
                
                nick_call = True
                _thread.start_new_thread(timer, ())
                nick_started = datetime.now()
                
            else:
                
                logging.warning("Attempt to call !nick - wrong symbol(s)")
                await msg.author.send("⛔ Ник не соответствует условиям (больше 2 символов, латиница, числа,\n отсутствие !@#$%^&*()-+=,.?/ \\ | []{}\'`~ \" )")
                
        else:
        
            now = datetime.now()
            diff = now - nick_started
            minutes = int((180 - diff.seconds)/60)
            seconds = int((180 - diff.seconds) - minutes*60)

            await msg.author.send("🕒 Данная команда станет доступна через " + str(minutes) + " минуты " + str(seconds) + " секунд")
            print("\n[" + now.strftime("%d-%m-%Y %H:%M:%S") + "] | Attempt to call new !nick task while previous in progress (will end in " + str(minutes) + " minutes " + str(seconds) + " seconds). Discord username - " + msg.author.name + "\n")
            logging.info("[" + now.strftime("%d-%m-%Y %H:%M:%S") + "] | Attempt to call new !nick task while previous in progress (will end in " + str(minutes) + " minutes " + str(seconds) + " seconds). Discord username - " + msg.author.name + "\n")



async def key(msg):
    global nick_call
    
    if nick_call == True:
        if msg.content.count("!key") == 1:
            #if msg.author.bot == True:
                global code
                global shodan_nick
                global game_nick
                global s
                global event1

                index = msg.content.find(':')
                shodan_nick = msg.content[0:index]

                if msg.content.endswith("!key " + str(code)):

                    if ("**" + game_nick + "**") == shodan_nick:

                        nick_call = False

                        await message_id.author.send("Верный ключ. Ваш ник изменен на " + game_nick + ". Приятного общения!")
                        await message_id.add_reaction('✅')

                        s.cancel(event1)

                        time = datetime.now()
                            
                        try:
                            await message_id.author.edit(nick= (game_nick + "_"))
                            print("\n[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] | Succesfull nick change. Discord username - " + message_id.author.name  + ". New Discord nickname - " + game_nick + "_")
                            logging.info("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] | Succesfull nick change. Discord username - " + message_id.author.name  + ". New Discord nickname - " + game_nick + "_")
                        except:
                            cprint('    \nBot is missing permissions. Try to switch the \'can change nicknames\' permission.', 'red')
                            
                    else:

                        nick_call = False

                        await message_id.author.send("⛔ Ваш ник не совпадает с ником игрока, которому был выдан код.")
                        await message_id.add_reaction('❌')

                        s.cancel(event1)

                        time = datetime.now()
                        
                        print("\n[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] | Unsuccesfull nick change due to different game nick. Discord username - " + message_id.author.name + ". Game nickname - " + shodan_nick + "")
                        logging.info("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] | Unsuccesfull nick change due to different game nick. Discord username - " + message_id.author.name + ". Game nickname - " + shodan_nick + "")

                else:

                    nick_call = False

                    await message_id.author.send("⛔ Неверный ключ.")
                    await message_id.add_reaction('❌')

                    s.cancel(event1)

                    time = datetime.now()
                    print("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] | Unsuccesfull nick change due to incorrect key. Discord username - " + message_id.author.name + ". Game nickname - " + shodan_nick + "")
                    logging.info("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] | Unsuccesfull nick change due to incorrect key. Discord username - " + message_id.author.name + ". Game nickname - " + shodan_nick + "")




# Событие сообщения В ЛЮБОМ канале группы дискорда ГДЕ у бота ЕСТЬ ДОСТУП НА ЧТЕНИЕ
@bot.event
async def on_message(msg):
    await bot.process_commands(msg)
    
    
    global gamechat_channel_id
    global main_channel_id
    
    
    """Реакции на ключевые слова, в общем канале"""
    if msg.channel.id == main_channel_id:
        
        f = '%H:%M:%S'
        now = datetime.strftime(datetime.now(), f)
        
        # Реакция текстом
        
        """Доброе утро @ник"""
        global goodmorn_first_use
        
        alarm = '08:00:00'
        diff = (datetime.strptime(alarm, f) - datetime.strptime(now, f))
        if msg.author.bot == False:
            if diff <= timedelta(hours= 2) and diff > timedelta(days= 0):
                if not goodmorn_first_use:
                    goodmorn_first_use = True
                    await msg.channel.send(msg.author.mention + " Доброе утро!")
            else:
                goodmorn_first_use = False
        
        
        
        """Спокойной ночи Норм Челам"""
        global goodnight_first_use
        
        alarm = '00:00:00'
        diff = (datetime.strptime(alarm, f) - datetime.strptime(now, f))
        
        if diff <= timedelta(hours= 1) and diff > timedelta(days= 0):
            if not goodnight_first_use:
                goodnight_first_use = True
                await msg.channel.send(":thumbsup: СПОКОЙНОЙ НОЧКИ НОРМЧЕЛЫ :thumbsup:")
        else:
            goodnight_first_use = False
        
        
        
        """Гайды"""
        if msg.content.count("как") or msg.content.count("Как") or msg.content.count("бьясните") or msg.content.count("бъясните") or msg.content.count("скажи"):
            """Гайд стрич овец"""
            if msg.content.count("стрич") >= 1 or msg.content.count("Стрич") >= 1 or msg.content.count("стрижк") >= 1 or msg.content.count("Стрижк") >= 1 :
                await msg.author.send("`Нажимайте с интервалом 0.5 секунд по овце ножом (каменным или металлическим) или ножницами`")
            if msg.content.count("выйти со спавна"):
                await msg.author.send("Со спавна есть две дороги - по морю (нужна лодка, идти по синим коврам, направо от точки спавна, вниз по лестнице в порт) или по суше (идти по коричневым коврам, налево от точки спавна, через мост Перерождения)")
        
        
        if msg.content.count("ртп") or msg.content.count("тепни"):
            await msg.author.send("Рандом телепорта НЕТ (/rtp), как и тп к другу (/tpa)! Большая часть мира - вода. Плывите в шлюпке или на корабле!")
        
        
        
        """В [50] % упоминаний вайпа бот напишет хуяйп"""
        if msg.content.count("вайп") >= 1 or msg.content.count("ВАЙП") >= 1 or msg.content.count("Вайп") >= 1  or msg.content.count("вАйп") >= 1 or msg.content.count("ваЙп") >= 1 or msg.content.count("вайП") >= 1 or msg.content.count("в.а.й.п") >= 1 or msg.content.count("В.А.Й.П") >= 1 or msg.content.count("в а й п") >= 1 or msg.content.count("В А Й П") >= 1 :

            a = random.randrange(0, 100)
            
            if a < 50:
                await msg.author.send("хуяйп")
        
        
        
        # Реакция картинками
        
        """А че сразу верд то?"""
        if msg.content.count("верд") >= 1 or msg.content.count("Werd") >= 1 or msg.content.count("Верд") >= 1 or msg.content.count("werd") >= 1 :

            a = random.randrange(0, 100)

            if a < 33:
                await msg.author.send(file=discord.File('imgs/werd.png'))
        
        
        
        """Дюпаешь?"""
        if msg.content.count("дюп") >= 1 :
            
            a = random.randrange(0, 100)
            
            if a < 33:
                await msg.author.send(file=discord.File('imgs/dyup.png'))
        
        
        
        """БАН"""
        if msg.content.count("бан") >= 1 :
            
            a = random.randrange(0, 100)
            
            if a < 80:
                await msg.author.send(file=discord.File('imgs/ban.png'))
        
        
        
        """В [30] % упоминаний пидор бот выберет пидора дня 'Пидор дня - @ник!', и на [50] % из этих упоминаний он ответит '@ник, а может быть ты пидор?'"""
        if msg.content.count("пидор") >= 1 :
            
            if msg.author.bot == False:
                #a = random.randrange(0, 100)
                
                global pidor_first_use
                global pidor_last_call
                
                diff = datetime.date(datetime.now()) - pidor_last_call
                
                if not pidor_first_use or diff >= timedelta(days=1):
                    #if a < 30:
                    x = msg.guild.members
                    lenght = len(x)
                    rnd = random.randrange(0, lenght)
                    
                    await msg.channel.send("Пидор Дня - " + str(x[rnd].mention) + " !")
                    logging.info("Pedo of the day is " + str(x[rnd]))
                    print("\nPedo of the day is " + str(x[rnd]))
                    
                    pidor_first_use = True
                    pidor_last_call = datetime.date(datetime.now())
                else:
                    b = random.randrange(0, 100)
                    if b < 50:
                        await msg.author.send(msg.author.mention + ", а может быть ты пидор?")
                    else:
                        await msg.author.send("Комманда Пидор Дня уже использовалась сегодня. Выберите Пидора завтра!")



    # Обработка ключа выданого по команде !nick [игровой_ник]
    if msg.channel.id == gamechat_channel_id:

        global nick_call

        if nick_call == True:
            
            if msg.content.count("!key") == 1:
            	await key(msg)


# ==========================================================================================================
print('\n------')
print('\n vk_group =  https://vk.com/club' + str(config.vk_group_id))
print('check delay - ' + str(config.check_delay) + ' sec')
print('\n------')

chat_ids = []
disc_channels = open(os.getcwd() + '/vkbot/disc_channels', 'r')
ids_arr = disc_channels.read().split(',')
print("\ndiscord_chat_ids:")
for i in ids_arr:
    if len(i) > 1:
        chat_ids.append(int(i))
        #channel = bot.get_channel(i)
        #print('name - ' + channel.name + ', id - ' + i)
        print(' id - ' + i)
disc_channels.close()
print('\n------')
pool = ThreadPool(4)

# получаем пост с заданым сдвигом
def get_post(offset=1):
    posts_offset = offset
    
    cooked = []
    a = urllib.request.urlopen('https://api.vk.com/method/wall.get?owner_id=-' + str(config.vk_group_id) + '&filter=owner&count=1&offset=' + str(posts_offset) + '&access_token=' + str(config.access_token) + '&v=' + str(config.vkapi_version))
    out = a.read().decode('utf-8')
    #print('--')
    #print('\n https://api.vk.com/method/wall.get?owner_id=-' + str(vk_group_id) + '&filter=owner&count=1&offset=' + str(posts_offset) + '&access_token=' + str(access_token) + '&v=' + str(vkapi_version) + ' \n')
    #print('\n--')
    
    json_data = json.loads(out)
    
    # получаем сырой текст
    text = json_data['response']['items'][0]["text"]
    #id_from_id = str(json_data['response']['items'][0]["from_id"])
    
    # убираем html требуху
    text = text.replace('<br>', '\n')
    text = text.replace('&amp', '&')
    text = text.replace('&quot', '"')
    text = text.replace('&apos', "'")
    text = text.replace('&gt', '>')
    text = text.replace('&lt', '<')

    # если встречается ссылка на профиль
    profile_to_replace = re.findall(r'\[(.*?)\]', text)
    profile_link = re.findall(r'\[(.*?)\|', text)
    profile_name = re.findall(r'\|(.*?)\]', text)
    profiles = []

    # заменаем ссылку на профиль в тексте
    try:
        for i in range(len(profile_link)):
            profiles.append(profile_name[i] + " (@" + profile_link[i] + ")")
        counter = 0
        for i in profile_to_replace:
            text = text.replace("[" + i + "]", profiles[counter])
            counter += 1
    except:
        pass

    #text += u"\n\nКомментарии: http://vk.com/wall" + id_from_id
    cooked.append(text)
    cooked.append(json_data['response']['items'][0]["date"])
    cooked.append(json_data['response']['items'][0]["id"])

    # на случай встречи с медиафайлами (пока что реализованы фото и тамб к видео)
    try:
        attachments = json_data['response']['items'][0]["attachments"]

        media_arr = []
        for media in attachments:
            if "photo" in media:
                media_arr.append(media["photo"]["sizes"][(len(media["photo"]["sizes"]) - 1)]["url"])
                # TODO "attachments": [ {"type":"photo","photo":{"sizes":[{"height":max,"url":"...\/...","type":"x","width":max}, {snd image}]
            #if "video" in media:
                #media_arr.append("http://vk.com/video" + media["video"]["owner_id"] + "_" + media["video"]["vid"])
            #if "doc" in media:
                #media_arr.append(media["doc"]["url"])
        cooked.append(media_arr)
    except:
        pass
    # cooked [text, timestamp, post_id, media_arr]
    return cooked
    
    
    
    
    
    
    
    
    
    
# проверяем новые посты
async def checker():
    await bot.wait_until_ready()
    
    if len(chat_ids) < 1:
        return
    
    with open(os.getcwd() + '/vkbot/last_post_id', 'r') as t:
        last_post_id = int(t.read())

    while not bot.is_closed():
        #print('\nchecking... ' + str(datetime.now()) + '__' + str(time.time()))
        
        #last_posts = 1
        #is_pinned = 1
        
        # берем закреп пост (потенциальный)
        pinned_post = get_post(0)
        # берем первый пост
        fst_post = get_post(1)
        
        # определяем есть закреп или нет
        #print('if pinned_id = ' + str(pinned_post[2]) + ' <= fst_id = ' + str(fst_post[2]))
        # если ид поста в закрепе старее чем ид первого поста
        if pinned_post[2] <= fst_post[2]:
            # установка для стены с закрепом
            is_pinned = 1
            # is_pinned = (если нет закрепа = 0)(если есть закреп = 1)

            #print('has_pinned')
        else:
            # установка для стены без закрепа
            is_pinned = 0
            # is_pinned = (если нет закрепа = 0)(если есть закреп = 1)
        last_posts = is_pinned


        end = False
        
        # проверяем новые новости по таймстампу и получаем количество новых
        while not end:
            # если есть закреп то проверяем 1-й пост, если нет то 0-й
            post = get_post(last_posts)
            
            # проверка на ласт пост (сверка с таймстампом в файле)
            #print('post = ' + str(post[2]) + '  >  last_post_id = ' + str(last_post_id))
            # если время в посте новее чем время в файле
            if post[2] > last_post_id:
                # если пост новее таймстампа
                #print('found +1 new post')
                
                last_posts += 1
                # ищем еще новые посты...
            else:
                # если таймстамп старше поста
                #print('found old post')
                # то это последний отправленный пост (время публикации которого запомнили в файле)
                
                # берем вторую границу 0-й или 1-й пост

                last = get_post(is_pinned)
                
                last_post_id = last[2]
                # запоминаем время 0-го или 1-го поста
                with open(os.getcwd() + '/vkbot/last_post_id', 'w') as t:
                    t.write(str(last_post_id))
                # завершаем цикл поиска новых постов
                end = True
        
        # выводим сообщение о найденых новых постах


        if last_posts > is_pinned:
            print('\nfound ' + str(last_posts - is_pinned) + ' new posts!')
            print('time: ' + str(datetime.now()) + '__' + str(time.time()) + '\n')
        
        # определяем условие отправки найденых постов
        # last_posts = 1+ если нет закрепа
        # last_posts = 2+ если есть закреп
        #print('is_pinned = ' + str(is_pinned))
        #print('last_posts = ' + str(last_posts))
        if last_posts > is_pinned:
        # рассылаем каждому нужное кол-во новых постов
            cprint('sending...\n', 'green')
            text_to_send = []
            timestamps = []
            post_ids = []
            
            # от 0 до [найденых постов -1(только если есть закреп)]
            for post_cur in range(last_posts - is_pinned):
                # берем пост (всего постов -1 -курсор(от 0 до [найденых постов -1(только если есть закреп)])
                post = get_post(last_posts - 1 - post_cur)
                # заполняем массив текста для поэтапной отправки
                text_to_send.append(post[0])
                timestamps.append(post[1])
                post_ids.append(post[2])
                
                # если в массиве поста есть фото
                photo_to_send = []
                if len(post) > 3:
                    for i in post[3]:
                        photo_to_send.append(i)
            
            # собственно попытка отправки
            try:
                # для всех каналов (ид которых взяты из файла ids)
                for ids_cur in range(len(chat_ids)):
                    # задаем переменную канала
                    channel = bot.get_channel(chat_ids[ids_cur])
                    #print('trying to send. channel name - ' + str(channel.name) + ', channel_id - ' + str(chat_ids[ids_cur]))
                    # для каждого текста в масиве текстов
                    for text_cur in range(len(text_to_send)):
                        embedVar = discord.Embed(title="", description=str("[Посмотреть на стене](https://vk.com/club" + config.vk_group_id + "?w=wall-" + config.vk_group_id + "_" + str(post_ids[text_cur]) + ")" + "\n\n" + text_to_send[text_cur]), color=0x00ff00)
                        embedVar.timestamp = datetime.fromtimestamp(timestamps[text_cur])
                        
                        if str(text_to_send[text_cur]) != '':
                            await channel.send(embed=embedVar)
                            
                        if photo_to_send:
                            for i in photo_to_send:
                                embedVar = discord.Embed(title="", description=str("[Посмотреть на стене](https://vk.com/club" + config.vk_group_id + "?w=wall-" + config.vk_group_id + "_" + str(post_ids[text_cur]) + ")" + "\n\n"), color=0x00ff00)
                                embedVar.timestamp = datetime.fromtimestamp(timestamps[text_cur])
                                embedVar.set_image(url=str(i))
                                await channel.send(embed=embedVar)
                                #await channel.send(str(i))
                                #yield from client.send_file(client.get_channel(str(id_)), str(i))
                
                print('      ')
                for text_cur in range(len(text_to_send)):
                    if str(text_to_send[text_cur]) != '':
                        pass
                        #cprint('text was sent -' + str(text_to_send[text_cur]) + '~', 'green')
                    else:
                        pass
                
                cprint('sent...', 'green')
            except:
                cprint('\nException while sending...\n', 'red')
        
        #print('------')
        
        # спим 1 минут
        await asyncio.sleep(config.check_delay)
        
bot.loop.create_task(checker())

bot.run(BOT_TOKEN)
