import time, sched, random
from datetime import datetime, timedelta, date
import _thread
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import logging
logging.basicConfig(filename='tfc.su_bot_test.log',level=logging.INFO)


client = discord.Client()


main_channel_id = 679093771908153355 #679093771908153355 - канал #основной или #общий
gamechat_channel_id = 679093832440348683 #679093832440348683 - канал #чат-игры


code = random.randrange(10000, 100000)
game_nick = ""
shodan_nick = ""
message_id = 1
nick_call = False
s = sched.scheduler(time.time, time.sleep)
event1 = None
delay_ended = False
nick_started = datetime.now()


TOKEN = ''


bot = commands.Bot(command_prefix='!') #инициализируем бота с префиксом '!'


@bot.event
async def on_ready():

    time = datetime.now()
    print("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] | Bot is online. Waiting for commands.\n") #Сообщение в консоль при завершении загрузки бота
    logging.info("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] | Bot is online. Waiting for commands.\n")
    channel = bot.get_channel(main_channel_id)
    await channel.send("Я в сети! Список комманд - !help")


#@bot.command(pass_context= True)
async def test(msg, *args): #проверка новых функций

    global main_channel_id

    if msg.channel.id == main_channel_id:

        if not args:

            await msg.channel.send("Try using an argument. For example: !test yes")

        elif args[0] == "yes":

            await msg.channel.send("This is a valid argument!")

        else:

            await msg.channel.send("Not a valid argument!")


dup_last_call = datetime.date(datetime.now())
dup_first_use = False

async def dupe(msg):
    """Дюпаешь? (алиасы - d, dup);"""
    global main_channel_id
    
    global dup_first_use
    global dup_last_call
    
    diff = datetime.date(datetime.now()) - dup_last_call
    
    if not dup_first_use or diff >= timedelta(minutes=60):
        if msg.channel.id == main_channel_id:
            await msg.channel.send(file=discord.File('dyup.png'))
            dup_first_use = True
            dup_last_call = datetime.date(datetime.now())


@bot.command(aliases= ['m'])
async def map(msg):
    await msg.channel.send("Карта (by xelo, SushiMan) - http://sushiweb.pp.ua/")


@bot.command(pass_context= True)
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


def strfdelta(tdelta, fmt):
    rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)


def timer():
    global s
    global event1

    event1 = s.enter(180, 1, flip_flop)
    s.run()


def flip_flop():
    global nick_call
    global delay_ended

    delay_ended = True
    nick_call = False

    time = datetime.now()
    print("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] | Previous !nick task was cancelled due to timeout.\n")
    logging.info("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] | Previous !nick task was cancelled due to timeout.\n")
    


pidor_last_call = datetime.date(datetime.now())
pidor_first_use = False

goodnight_first_use = False
goodmorn_first_use = False


@bot.event
async def on_message(msg):
    await bot.process_commands(msg)

    global gamechat_channel_id
    global main_channel_id
    
    if msg.channel.id == main_channel_id:
    
        f = '%H:%M:%S'
        now = datetime.strftime(datetime.now(), f)
        
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
        
        """Гайд стрич овец"""
        if msg.content.count("стрич овец") >= 1 or msg.content.count("Стрич овец") >= 1 or msg.content.count("стрижка овец") >= 1 or msg.content.count("Стрижка овец") >= 1 :
            await msg.author.send("`Нажимайте с интервалом 0.5 секунд по овце ножом (каменным или металлическим) или ножницами`")

        """В 20 % упоминаний вайпа бот напишет хуяйп"""
        if msg.content.count("вайп") >= 1 or msg.content.count("ВАЙП") >= 1 or msg.content.count("Вайп") >= 1  or msg.content.count("вАйп") >= 1 or msg.content.count("ваЙп") >= 1 or msg.content.count("вайП") >= 1 or msg.content.count("в.а.й.п") >= 1 or msg.content.count("В.А.Й.П") >= 1 or msg.content.count("в а й п") >= 1 or msg.content.count("В А Й П") >= 1 :

            a = random.randrange(0, 100)
            
            if a < 20:
                await msg.channel.send("хуяйп")

        """А че сразу верд то?"""
        if msg.content.count("верд") >= 1 or msg.content.count("Werd") >= 1 or msg.content.count("Верд") >= 1 or msg.content.count("werd") >= 1 :

            a = random.randrange(0, 100)

            if a < 20:
                await msg.channel.send(file=discord.File('werd.png'))

        """Дюпаешь?"""
        if msg.content.count("дюп") >= 1 :
            
            a = random.randrange(0, 100)
            
            if a < 20:
                await msg.channel.send(file=discord.File('dyup.png'))

        """В 30 % упоминаний пидор бот выберет пидора дня 'Пидор дня - @ник!', и на 50 % из этих упоминаний он ответит '@ник, а может быть ты пидор?'"""
        if msg.content.count("пидор") >= 1:
            
            if msg.author.bot == False:
                a = random.randrange(0, 100)
                
                global pidor_first_use
                global pidor_last_call
                
                diff = datetime.date(datetime.now()) - pidor_last_call
                
                if not pidor_first_use or diff >= timedelta(days=1):
                    if a < 30:
                        x = msg.guild.members
                        lenght = len(x)
                        rnd = random.randrange(0, lenght)
                        
                        await msg.channel.send("Пидор Дня - " + str(x[rnd].mention) + " !")
                        logging.info("\nPedo of the day is " + str(x[rnd]))
                        print("\nPedo of the day is " + str(x[rnd]))
                        
                        pidor_first_use = True
                        pidor_last_call = datetime.date(datetime.now())
                else:
                    b = random.randrange(0, 100)
                    if b < 50:
                        await msg.channel.send(msg.author.mention + ", а может быть ты пидор?")
                    else:
                        await msg.author.send("Комманда Пидор Дня уже использовалась сегодня. Выберите Пидора завтра!")

    """Обработка ключа"""
    if msg.channel.id == gamechat_channel_id:

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
                            print("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] | Succesfull nick change. Discord username - " + message_id.author.name  + ". New Discord nickname - " + game_nick + "_")
                            logging.info("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] | Succesfull nick change. Discord username - " + message_id.author.name  + ". New Discord nickname - " + game_nick + "_")

                            await message_id.author.edit(nick= (game_nick + "_"))

                        else:

                            nick_call = False

                            await message_id.author.send("⛔ Ваш ник не совпадает с ником игрока, которому был выдан код.")
                            await message_id.add_reaction('❌')

                            s.cancel(event1)

                            time = datetime.now()
                            print("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] | Unsuccesfull nick change due to different game nick. Discord username - " + message_id.author.name + ". Game nickname - " + shodan_nick + "")
                            logging.info("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] | Unsuccesfull nick change due to different game nick. Discord username - " + message_id.author.name + ". Game nickname - " + shodan_nick + "")

                    else:

                        nick_call = False

                        await message_id.author.send("⛔ Неверный ключ.")
                        await message_id.add_reaction('❌')

                        s.cancel(event1)

                        time = datetime.now()
                        print("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] | Unsuccesfull nick change due to incorrect key. Discord username - " + message_id.author.name + ". Game nickname - " + shodan_nick + "")
                        logging.info("[" + time.strftime("%d-%m-%Y %H:%M:%S") + "] | Unsuccesfull nick change due to incorrect key. Discord username - " + message_id.author.name + ". Game nickname - " + shodan_nick + "")


bot.run(TOKEN)
