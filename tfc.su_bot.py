# -*- coding: utf-8 -*
'''
Created on 11 окт. 2020 г.

@author: User
'''
import time, sched, random
from random import choice
from datetime import datetime, timedelta, date
import _thread
import logging
import sys

import discord
from discord.ext import commands
from discord.ext.commands import Bot

# =============================================================================================

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', help_command=None, intents=intents) #инициализируем бота с префиксом '!'

# Конфигурация
# =============================================================================================
BOT_TOKEN = ''
#main
main_channel_id = 764106268780396574 #644905699436134400 - канал #основной или #общий
gamechat_channel_id = 764103166072717322 #542326584422563850 - канал #чат-игры

#logging.basicConfig(filename='tfc.su_bot.log',level=logging.INFO)







print("\n[" + str(time.strftime("%d-%m-%Y %H:%M:%S")) + "] | Script start")
# Событие входа бота в онлайн
@bot.event
async def on_ready():

    time = datetime.now()
    print("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] | Bot is online. Waiting for commands.\n") #Сообщение в консоль при завершении загрузки бота
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
    rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)


# таймер 3 мин после чего включить функцию flip_flop
def timer():
    global s
    global event1

    event1 = s.enter(180, 1, flip_flop)
    s.run()


# переключение таймера изза неактивности после выдачи кода
def flip_flop():
    global nick_call
    global delay_ended

    delay_ended = True
    nick_call = False

    time = datetime.now()
    print("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] | Previous !nick task was cancelled due to timeout.\n")
    logging.info("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] | Previous !nick task was cancelled due to timeout.\n")
    
# =====================================================================================


    
# принудительно выключаем программу
@bot.command()
async def halt(msg):
    sys.exit()
    
    
    
@bot.command()
async def test(msg):
    await msg.author.send("test")
    embedVar = discord.Embed(title="Title", description="Desc", color=0x00ff00)
    embedVar.set_image(url="https://pbs.twimg.com/profile_images/1311725514814521347/L2UDOARa_400x400.jpg")
    embedVar.add_field(name="Field1", value="hi", inline=False)
    embedVar.add_field(name="Field2", value="hi2", inline=False)
    await msg.channel.send(embed=embedVar)
    
    
    
#@bot.command(pass_context= True)
async def arguments(msg, *args): #проверка новых функций

    global main_channel_id

    if msg.channel.id == main_channel_id:

        if not args:

            await msg.channel.send("Try using an argument. For example: !test yes")

        elif args[0] == "yes":

            await msg.channel.send("This is a valid argument!")

        else:

            await msg.channel.send("Not a valid argument!")
    
    
    
 

    
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

                logging.warning("Attempt to call !nick - no arguments")
                await msg.author.send("⛔ Укажите свой игровой ник !nick nickname.")

            elif len(args[0]) >= 2 and not args[0].count("@") and not args[0].count("!") and not args[0].count("#") and not args[0].count("$") and not args[0].count("%") and not args[0].count("^") and not args[0].count("&") and not args[0].count("*") and not args[0].count("(") and not args[0].count(")") and not args[0].count("-") and not args[0].count("+") and not args[0].count("=") and not args[0].count(",") and not args[0].count(".") and not args[0].count("/") and not args[0].count("?") and not args[0].count("/") and not args[0].count("\\") and not args[0].count("|") and not args[0].count("[") and not args[0].count("]") and not args[0].count("{") and not args[0].count("}") and not args[0].count("\'") and not args[0].count("\"") and not args[0].count("`") and not args[0].count("~") :

                global game_nick
                global code
                global delay_ended

                if delay_ended == True:
                    delay_ended = False
                    await message_id.add_reaction('🕒')

                message_id = msg.message
                print(msg.message)
                game_nick = args[0]
                code = random.randrange(10000, 100000)

                await msg.author.send("Напишите этот ключ в глобальный чат игры - " + "!key " + str(code))

                time = datetime.now()
                print("\n[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] | New !nick task. Waiting for !key command. Discord username - " + message_id.author.name + ". Entered nickname - " + game_nick + ".")
                logging.info("\n[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] | New !nick task. Waiting for !key command. Discord username - " + message_id.author.name + ". Entered nickname - " + game_nick + ".")

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
            logging.info("\n[" + now.strftime("%d-%m-%Y %H:%M:%S") + "] | Attempt to call new !nick task while previous in progress (will end in " + str(minutes) + " minutes " + str(seconds) + " seconds). Discord username - " + msg.author.name + "\n")

            
            
            
            
            

async def key(msg):
    global nick_call
    
    if nick_call == True:
        if msg.content.count("!key") == 1:
            if msg.author.bot == True:
                global code
                global shodan_nick
                global game_nick
                global s
                global event1

                index = msg.content.find(':')
                shodan_nick = msg.content[0:index]
                #message_obj = bot.get_channel(main_channel_id).fetch_message(message_id)

                if msg.content.endswith("!key " + str(code)):

                    if ("**" + game_nick + "**") == shodan_nick:

                        nick_call = False

                        await message_id.author.send("Верный ключ. Ваш ник изменен на " + game_nick + ". Приятного общения!")
                        await message_id.add_reaction('✅')

                        s.cancel(event1)

                        time = datetime.now()
                            
                        try:
                            await message_id.author.edit(nick= (game_nick + "_"))
                            print("\n [" + time.strftime("%d-%m-%Y %H:%M:%S") + "] | Succesfull nick change. Discord username - " + message_id.author.name  + ". New Discord nickname - " + game_nick + "_")
                            logging.info("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] | Succesfull nick change. Discord username - " + message_id.author.name  + ". New Discord nickname - " + game_nick + "_")
                        except:
                            cprint('    \nBot is missing permissions. Try to switch the \'can change nicknames\' permission.', 'red')
                            
                    else:

                        nick_call = False

                        await message_id.author.send("⛔ Ваш ник не совпадает с ником игрока, которому был выдан код.")
                        await message_id.add_reaction('❌')

                        s.cancel(event1)

                        time = datetime.now()
                        
                        print("\n [" + time.strftime("%d-%m-%Y %H:%M:%S") + "] | Unsuccesfull nick change due to different game nick. Discord username - " + message_id.author.name + ". Game nickname - " + shodan_nick + "")
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
        
        
        
        """В 20 % упоминаний вайпа бот напишет хуяйп"""
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



    """Обработка ключа"""
    if msg.channel.id == gamechat_channel_id:

        global nick_call

        if nick_call == True:
            
            if msg.content.count("!key") == 1:
            	await key(msg)

                        


bot.run(BOT_TOKEN)
