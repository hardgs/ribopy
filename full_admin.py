from rubpy import Client,filters # pip3 install rubpy
from rubpy.types import Update # pip3 install rubpy
from NightDB import NightDB
from httpx import AsyncClient # pip3 install httpx
from asyncio import sleep
import utills


print("Initing ENV...")
admins = ["u0DsXjn0fe84d636cf1f42a0cb292693","u0DwuqS017f68d4545e326e0bbcd9ca6"]
config = {
    "channel":"c0CPOlg02db41ed2e478961d720f330f",
    "usdid":"1093267119967785",
    "prdsave":"c0CPlFv09746422e4b7f4861036a3e29",
    "allorder":108,
    "upload":"c0Bu1ir08f8820ca04ab1d452a13e6ee"
}

statusIncome = {
    "sizeorder":0,
    "corder":0,
    "norder":0,
    "income":0,
    "cost":79000,
    "money":0
}
db = NightDB()
db.read("""guid,look_link,look_forward,look_image,look_gif,look_voice,look_video,look_insuit
g0CxR4B0d5fb9c244cb1bea769da8d40,True,True,False,False,False,False,True
""")
groups = db.get_colums("guid")

bot = Client("manager.rp")
is_autoupdate = False


async def get_admins(object_guid: str):
    global bot
    try:
        members = (await bot.get_group_admin_members(object_guid))["in_chat_members"]
    except:
        members = []
    result = []
    for member in members:
        result.append(member["member_guid"])
    return result

async def is_admin(object_guid: str,auther_guid: str):
    if not object_guid in utills.admins:
        utills.admins[object_guid] = {"last_update":int(utills.time()),"members":await get_admins(object_guid)}
    else:
        if (int(utills.time())-utills.admins[object_guid]["last_update"]) >= 3600:
            utills.admins[object_guid]["members"] = await get_admins(object_guid)
    for member in utills.admins[object_guid]["members"]:
        if auther_guid == member:
            return True
    return False

# Shop Commands
# Parsing AnD Execute Admins Commands
@bot.on_message_updates(filters.is_private,filters.is_me,filters.commands("order","/"))
async def add_order(update: Update):
    await update.delete()
    orderID = config["allorder"]+1
    config["allorder"]+=1
    statusIncome["norder"]+=1
    statusIncome["sizeorder"]+=1
    orderPrice = int(update.text.split(" ")[1])
    username = (await bot.get_user_info(update.object_guid))["user"]
    if("username" in username):
        username = username["username"]
    else:
        username="NULL"
    msgID = await bot.send_message(config["prdsave"],f"""
•
🛍| #order #product
 {update.object_guid}

🆔| @{username}
📦| **orderID**: `{orderID}`
❌| #need_complete
💵| Price: {str(orderPrice)}
°
""")
    msgID = msgID["message_update"]["message_id"]
    await bot.send_message(update.object_guid,f"""{msgID},{str(orderPrice)}

       سفارش شما با موفقیت **ثبت** شد ✅
   📦| کد سفارش: **{orderID}**
   **تا امدن پیام بعدی صبر کنید**
""")
    
@bot.on_message_updates(filters.is_private,filters.commands("complete","/"))
async def complete_order(update: Update):
    await update.delete()
    if hasattr(update,"reply_to_message_id"):
        msgText = (await bot.get_messages_by_id(update.object_guid,[update.reply_message_id]))["messages"][0]["text"]
        msgID=""
        msgPrice =0
        simtext = ""

        # Get Message ID
        for c in msgText:
            if c=="\n":
                msgPrice = int(simtext)
                del(simtext)
                break
            if c==",":
                msgID = simtext
                simtext = ""
                continue
            simtext = simtext + c
        
        # Setting Status Of Store
        statusIncome["money"]+=msgPrice
        statusIncome["norder"]-=1
        statusIncome["corder"]+=1
        
        # Get Message Text Of Product
        msgText = (await bot.get_messages_by_id(config["prdsave"],[msgID]))["messages"][0]["text"]
        msgText = msgText.replace("#need_complete","#complete")
        msgText = msgText.replace("❌","✅")

        # Edit Message
        await bot.edit_message(config["prdsave"],msgID,msgText)

        # And Send Last Message
        await bot.send_message(update.object_guid,"""
سفارش شما با موفقیت انجام شد✅

     ایا ازمن یعنی PharaohShop | فرعون شاپ راضی هستین؟
 
    عکس از اکانت شما فراموش نشود😅
     
🌐| @pharaohshop
👤| @pharaohshop_admin
""",update.reply_message_id)

@bot.on_message_updates(filters.is_private,filters.commands("incomplete","/"))
async def send_incoming_msg(update: Update):
    await update.delete()
    # And Send Last Message
    await bot.send_message(update.object_guid,"""
      سفارش شما در حال انجام دادن است✅
""")

@bot.on_message_updates(filters.is_private,filters.commands("uid","/"))
async def send_uid_msg(update: Update):
    await update.delete()
    # And Send Last Message
    await bot.send_message(update.object_guid,"""
   اطلاعات زیر بفرستید
   
  🆔| UID: ایدی اکانت
  👤| Name: نام اکانت
  🖼️| Photo: عکس از پروفایل اکانت
""")

@bot.on_message_updates(filters.is_private,filters.commands("gmail","/"))
async def send_gmail_msg(update: Update):
    await update.delete()
    # And Send Last Message
    await bot.send_message(update.object_guid,"""
   اطلاعات زیر بفرستید
   
  📧| EMAIL: ایمیل اکانت
  🔑| Password: رمز ایمیل
  🗝️| Backup: کد بک اپ
  
  👤| Name: نام اکانت
  🆔| UID: نام ایدی اکانت
  🖼️| Photo: عکس از پروفایل اکانت
""")

@bot.on_message_updates(filters.is_private,filters.commands("ffcard","/"))
async def send_ffcard_msg(update: Update):
    await update.delete()
    # And Send Last Message
    await bot.send_message(update.object_guid,"""
    💳| شماره کارت
    
  COPY:  «`5022291536400151`»
    READ:  «5022 2915 3640 0151»
    
    به نام : مهند جنامی
    
      🔑عکس از رسید یادت نره√
👤|PV: @pharaohshop_admin
""")
    
@bot.on_message_updates(filters.is_private,filters.commands("cpcard","/"))
async def send_cpcard_msg(update: Update):
    await update.delete()
    # And Send Last Message
    await bot.send_message(update.object_guid,"""
    💳| شماره کارت
    
  COPY:  «`5022291535300360`»
    READ:  «5022 2915 3530 0360»
    
    به نام : جواد موسی زاده
    
      🔑عکس از رسید یادت نره√
👤|PV: @pharaohshop_admin
""")

@bot.on_message_updates(filters.is_private,filters.commands("check","/"))
async def send_incoming_msg(update: Update):
    await update.delete()
    # And Send Last Message
    await bot.send_message(update.object_guid,"""
    سفارش شما در حال برسی است ✅
    لطفا یکم صبور باشین🙏
""")

# Group Management Commands
@bot.on_message_updates(filters.is_group(groups),filters.commands(["help","راهنما"],''))
async def send_global_help(update: Update):
    if not update.object_guid in groups:
        return None
    await sleep(utills.randint(1,5))
    await update.reply("""**راهنما عمومی:**
دستورات زیر جهت سرگرمی هستن
• نام
• جوک
• دانستنی
• ایا میدانی
• بیو
• ذکر
• حدیث
• الودگی [شهر مورد نظر]
• مناسبات روز
• اوقات شرعی [اینجا شهر مورد نظر وارد کنید]
• داستان
• زمان
و برای ادمینا دستور زیر بفرسته
• /help
""")

@bot.on_message_updates(filters.is_group(groups),filters.commands("مناسبات روز",''))
async def send_monasbat(update: Update):
    if not update.object_guid in groups:
        return None
    async with AsyncClient() as client:
        result = (await client.get("https://api.codebazan.ir/monasebat/")).json()
    atext = "📆| مناسبات روز \n"
    for r in result:
        atext+=r["occasion"]+"\n**+**\n"
    await sleep(utills.randint(1,3))
    await update.reply(atext)

@bot.on_message_updates(filters.is_group(groups),filters.commands(["bio","بیو"],''))
async def send_bio(update: Update):
    if not update.object_guid in groups:
        return None
    await sleep(utills.randint(1,5))
    async with AsyncClient() as client:
        await update.reply((await client.get("https://api.codebazan.ir/bio/")).text)

@bot.on_message_updates(filters.is_group(groups),filters.commands(["jok","جوک"],''))
async def send_jok(update: Update):
    if not update.object_guid in groups:
        return None
    await sleep(utills.randint(1,5))
    async with AsyncClient() as client:
        result = (await client.get("http://api.codebazan.ir/jok/")).text
    await update.reply("📝| جوک\n"+result)

@bot.on_message_updates(filters.is_group(groups),filters.commands(["name","نام"],''))
async def send_name(update: Update):
    if not update.object_guid in groups:
        return None
    await sleep(utills.randint(1,3))
    async with AsyncClient() as client:
        await update.reply((await client.get("https://api.codebazan.ir/name/")).text)

@bot.on_message_updates(filters.is_group(groups),filters.commands(["story","داستان"],''))
async def send_story(update: Update):
    if not update.object_guid in groups:
        return None
    result = "📝| داستان \n"
    async with AsyncClient() as client:
        result += (await client.get("http://api.codebazan.ir/dastan/")).text
    await sleep(utills.randint(1,3))
    await update.reply(result)

@bot.on_message_updates(filters.is_group(groups),filters.commands(["dialog","دیالوگ"],''))
async def send_dialog(update: Update):
    if not update.object_guid in groups:
        return None
    result = "📝| دیالوگ \n"
    async with AsyncClient() as client:
        result += (await client.get("http://api.codebazan.ir/dialog/")).text
    await sleep(utills.randint(1,5))
    await update.reply(result)

@bot.on_message_updates(filters.is_group(groups),filters.commands(["zekr","ذکر"],''))
async def send_zekr(update: Update):
    if not update.object_guid in groups:
        return None
    async with AsyncClient() as client:
        result = (await client.get("http://api.codebazan.ir/zekr/")).text
    await sleep(utills.randint(1,3))
    await update.reply(result)

@bot.on_message_updates(filters.is_group(groups),filters.commands(["hadis","حدیث"],''))
async def send_hadith(update: Update):
    # Need Update
    if not update.object_guid in groups:
        return None
    async with AsyncClient() as client:
        result = (await client.get("https://api.keybit.ir/hadis/")).json()["result"]
    await sleep(utills.randint(1,3))
    await update.reply(f"""
📝| حدیث هفته 

** {result['text']} **

✍️ ~ {result["person"]}
🌙 ~ منبع: {result["source"]}
""")
@bot.on_message_updates(filters.is_group(groups),filters.commands(["ayamedani","ایامیدانی","ایا می دانی","ایا میدانی"],''))
async def send_fact2(update: Update):
    if not update.object_guid in groups:
        return None
    async with AsyncClient() as client:
        result = (await client.get(f"https://api.keybit.ir/ayamidanid")).json()
        await update.reply("""
📝| ایا میدانی؟

** result['text'] **
""")


@bot.on_message_updates(filters.is_group(groups),filters.commands(["time","زمان"],''))
async def send_time(update: Update):
    if not update.object_guid in groups:
        return None
    async with AsyncClient() as client:
        result = (await client.get("http://api.codebazan.ir/time-date/?json=fa")).json()
    if result["ok"]:
        result = result["result"]
        await sleep(utills.randint(1,3))
        await update.reply(f"""
• ⏰ | زمان: {result["time"]}
• 📆 |تاریخ: {result["date"]}
• 🏞️ | فصل: {result["fasl"]}
• 👀 | {result["weekname"]}
• 📅 | {result["mahname"]}
""")

@bot.on_message_updates(filters.is_group(groups),filters.commands(["fact","دانستنی"],''))
async def send_fact(update: Update):
    if not update.object_guid in groups:
        return None
    result = "📝| دانستنی \n"
    async with AsyncClient() as client:
        result += (await client.get("http://api.codebazan.ir/danestani/")).text
    await sleep(utills.randint(1,5))
    await update.reply(result)
@bot.on_message_updates(filters.is_group(groups),filters.commands(["الودگی","آلودگی"],''))
async def send_aqms(update: Update):
    if not update.object_guid in groups:
        return None
    city = update.text.split(" ")[1]
    stations = []
    for station in utills.aqms:
        if city in station["StationName_Fa"]:
            stations.append(station)
    result = "☁️| الودگی هوا\n"
    for station in stations:
        result += f"""
💨 • ** {station["StationName_Fa"]} **
🌫️ • شاخص ** {station["AQI"]} AQI **

"""
    await sleep(utills.randint(1,3))
    await update.reply(result)
@bot.on_message_updates(filters.is_group(groups),filters.commands("اوقات شرعی",''))
async def send_timetable(update: Update):
    if not update.object_guid in groups:
        return None
    city = update.text.split(" ")
    if len(city)==3:
        async with AsyncClient() as client:
            result = (await client.get("https://api.codebazan.ir/owghat/?city="+city[2])).json()["Result"][0]
        await sleep(utills.randint(1,3))
        await update.reply(f"""
    • 📅| اوقات شرعی 

    • 🏙️| شهر: {result["shahr"]}
    • 📅| تاریخ: {result["tarikh"]}

    • 🌅| اذان صبح: {result["azansobh"]}
    • 🌄| طلوع افتاب: {result["toloaftab"]}
    • 🌅| اذان ظهر: {result["azanzohr"]}
    • 🌇| غروب افتاب: {result["ghorubaftab"]}
    • 🌆| اذان مغرب: {result["azanmaghreb"]}
    • 🌃| نیم شب: {result["nimeshab"]}
    """)
    elif len(city)==2:
        await sleep(utills.randint(1,3))
        await update.reply("""شهر مورد نظر وارد کنید
    اوقات شرعی [شهر مورد نظر]
""")

# Group Management Admin Methods
@bot.on_message_updates(filters.is_group(groups),filters.commands("ban","/"))
async def ban_user(update: Update):
    if not update.object_guid in groups:
        return None
    if await is_admin(update.object_guid,update.author_guid):
        if hasattr(update,"reply_to_message_id"):
            guid=await update.get_reply_author()
            guid = guid["user"]["user_guid"]
            await update.ban_member(user_guid=guid)

@bot.on_message_updates(filters.is_group(groups),filters.commands("unban","/"))
async def unban_user(update: Update):
    if not update.object_guid in groups:
        return None
    if await is_admin(update.object_guid,update.author_guid):
        if hasattr(update,"reply_to_message_id"):
            guid=await update.get_reply_author()
            guid = guid["user"]["user_guid"]
            await update.unban_member(user_guid=guid)

@bot.on_message_updates(filters.is_group(groups),filters.commands("pin","/"))
async def pin_user(update: Update):
    if not update.object_guid in groups:
        return None
    if await is_admin(update.object_guid,update.author_guid):
        if hasattr(update,"reply_to_message_id"):
            await update.pin(message_id=update.reply_message_id)
            await sleep(utills.randint(1,3))
            await update.reply("با موفقیت پین/سنجاق شده")
 
@bot.on_message_updates(filters.is_group(groups),filters.commands("unpin","/"))
async def unpin_user(update: Update):
    if not update.object_guid in groups:
        return None
    if await is_admin(update.object_guid,update.author_guid):
        if hasattr(update,"reply_to_message_id"):
            await update.unpin(message_id=update.reply_message_id)
            await sleep(utills.randint(1,3))
            await update.reply("با موفقیت لغو پین/سنجاق شده")

@bot.on_message_updates(filters.is_group(groups),filters.commands("look","/"))
async def look_anything(update: Update):
    if not update.object_guid in groups:
        return None
    if not await is_admin(update.object_guid,update.author_guid):
        return
    typeLook = update.text[6:]
    config = db.get_row_by_colum("guid",update.object_guid)
    config[f"look_{typeLook}"] = not config[f"look_{typeLook}"]
    #db.save("group.csv")
    if config[f"look_{typeLook}"]:
        await update.reply("با موفقیت قفل شده")
    else:
        await update.reply("با موفقیت باز شده")

@bot.on_message_updates(filters.is_group,filters.commands("status","/"))
async def send_status(update: Update):
    if not update.object_guid in groups:
        return None
    if not await is_admin(update.object_guid,update.author_guid):
        return
    def booltoEmoji(t):
        if t:
            return "✅"
        return "❌"
    row = db.get_row_by_colum("guid",update.object_guid)
    await sleep(utills.randint(1,3))
    await update.reply(f"""وضعیت قفل ها:

• قفل فوروارد: {booltoEmoji(row["look_forward"])}
• قفل لینک: {booltoEmoji(row["look_link"])}
• قفل فحش: {booltoEmoji(row["look_insuit"])}

• قفل عکس: {booltoEmoji(row["look_image"])}
• قفل ویس: {booltoEmoji(row["look_voice"])}
• قفل گیف: {booltoEmoji(row["look_gif"])}
• قفل ویدیو: {booltoEmoji(row["look_video"])}
""")


@bot.on_message_updates(filters.is_group,filters.commands("close","/"))
async def close_group(update: Update):
    if not update.object_guid in groups:
        return None
    if not await is_admin(update.object_guid,update.author_guid):
        return
    await bot.set_group_default_access(update.object_guid,[])
    await sleep(utills.randint(1,3))
    await update.reply("گروه با موفقیت بسته شد")

@bot.on_message_updates(filters.is_group,filters.commands("open","/"))
async def open_group(update: Update):
    if not update.object_guid in groups:
        return None
    if not await is_admin(update.object_guid,update.author_guid):
        return
    await bot.set_group_default_access(update.object_guid,["SendMessages"])
    await sleep(utills.randint(1,3))
    await update.reply("گروه با موفقیت باز شد")

@bot.on_message_updates(filters.is_group,filters.commands("help","/"))
async def send_help(update: Update):
    if not update.object_guid in groups:
        return None
    if not await is_admin(update.object_guid,update.author_guid):
        return
    await sleep(utills.randint(1,3))
    await update.reply("""**راهنما ادمین ها:**
`/pin`
• پین کردن پیام (حتما پیام مورد نظر ریپلای یا حالت پاسخ بزارید)
`/unpin`
• لغو پین یا سنجاق (حتما پیام مورد نظر ریپلای کنید)
`/ban` 
• بن کردن (حتما کاربر مورد نظر ریپلای کنید)
`/unban`
• لغو بن ( حتما کاربر مورد نظر ریپلای کنید)

`/open`
• باز کردن گروه
`/close`
• بستن گروه

**قفل ها:**
`/look link`
• قفل کردن لینک ها
`/look forward`
• قفل کردن فوروارد
`/look insuit`
• قفل کردن فحش ها

`/look image`
• قفل کردن عکس
`/look video`
• قفل کردن ویدیوها
`/look gif`
• قفل کردن گیف ها
`/look voice`
• قفل کردن ویس ها

`/status`
• وضعیت قفل ها
""")

# Group Management General Of Groups
@bot.on_message_updates(filters.is_group)
async def look_messages(update: Update):
    if not update.object_guid in groups:
        return None
    if(update.is_event):
        if(update["message"]["event_data"]["type"]=="LeaveGroup"):
            await update.reply(utills.speak["leave"][utills.randint(0,len(utills.speak["leave"])-1)])
        elif(update["message"]["event_data"]["type"]=="JoinedGroupByLink"):
            await update.reply(utills.speak["join"][utills.randint(0,len(utills.speak["join"])-1)])
        return None
    
    # Speaker
    if(update.is_text):
        text = utills.speak["text"]
        for key in list(text.keys()):
            if "#" in key:
                if key.replace("#","") == update.text:
                    await sleep(utills.randint(0,5))
                    await update.reply(text[key][utills.randint(0,len(text[key])-1)])
                    break
            elif key in update.text:
                await sleep(utills.randint(0,5))
                await update.reply(text[key][utills.randint(0,len(text[key])-1)])
                break
        if not update.reply_message_id==None:
            text = utills.speak["reply"]
            for key in list(text.keys()):
                if "#" in key:
                    if key.replace("#","") == update.text:
                        if update.get_reply_author()==utills.speak["guid"]:
                            await sleep(utills.randint(0,5))
                            await update.reply(text[key][utills.randint(0,len(text[key])-1)])
                            break
                elif key in update.text:
                    if (await update.get_reply_message())["author_object_guid"]==utills.speak["guid"]:
                        await sleep(utills.randint(0,5))
                        await update.reply(text[key][utills.randint(0,len(text[key])-1)])
                        break
    
    # Looker
    if await is_admin(update.object_guid,update.author_guid):
        return None
    
    config = db.get_row_by_colum("guid",update.object_guid)
    if update.is_text:
        if config["look_link"] and await utills.has_link(update.text):
            await update.delete()
        if config["look_insuit"] and await utills.has_insuit(update.text):
            await update.delete()
    elif config["look_forward"] and update.is_forward:
        await update.delete()
    elif update.is_file_inline:
        if config["look_image"] and update.file_inline.type=="Image":
            await update.delete()
        elif config["look_gif"] and update.file_inline.type=="Gif":
            await update.delete()
        elif config["look_voice"] and update.file_inline.type=="Voice":
            await update.delete()
        elif config["look_video"] and update.file_inline.type=="Vedio":
            await update.delete()
            
# Master Commands
@bot.on_message_updates(filters.object_guids(admins),filters.commands("gettable",'/'))
async def send_table(update: Update):
    await update.reply(db.save())
    await update.reply("با موفقیت جدول ارسال شد")

@bot.on_message_updates(filters.object_guids(admins),filters.commands("settable",'/'))
async def set_table(update: Update):
    global groups,db
    message=await update.get_reply_message()
    db.read(message["text"])
    groups = db.get_colums("guid")
    await update.seen()
    await update.reply("با موفقیت جدول ثبت شد")

@bot.on_message_updates(filters.object_guids(admins),filters.commands("joingroup",'/'))
async def join_group(update: Update):
    global groups,db
    link=update.text.split(" ")[1]
    try:
        guid = await bot.join_group(link)
        guid = guid["group"]["group_guid"]
        db.body.append({
                "guid":guid,
                "look_forward":True,
                "look_insuit":True,
                "look_link":True,
                "look_image":False,
                "look_gif":False,
                "look_voice":False,
                "look_video":False
            })
        groups.append(guid)
        await update.seen()
        await update.reply("با موفقیت لینک اضافه شد")
    except:
        await update.reply("خطا در جوین گروه ")
@bot.on_message_updates(filters.object_guids(admins),filters.commands("addbyguid",'/'))
async def add_by_guid(update: Update):
    global db,groups
    guid = update.text.split(' ')[1]
    db.body.append({
                "guid":guid,
                "look_forward":True,
                "look_insuit":True,
                "look_link":True,
                "look_image":False,
                "look_gif":False,
                "look_voice":False,
                "look_video":False
            })
    await update.seen()
    groups.append(guid)
@bot.on_message_updates(filters.object_guids(admins),filters.commands("getguidbylink","/"))
async def get_guid_by_link(update: Update):
    guid =  await bot.group_preview_by_join_link(update.text.split(' ')[1])
    await update.seen()
    await update.reply(guid["group"]["group_guid"])

@bot.on_message_updates(filters.object_guids(admins),filters.commands("textall","/"))
async def send_text_all(update: Update):
    text = await update.get_reply_message()
    text = text["text"]
    for guid in groups:
        try:
            await bot.send_message(guid,text)
        except:
            print(guid)
            print("ERROR: Above")

@bot.on_message_updates(filters.object_guids(admins),filters.commands("forwardall","/"))
async def forward_all(update: Update):
    text = await update.get_reply_message()
    for guid in groups:
        try:
            await bot.forward_messages(text["author_object_guid"],guid,[text["message_id"]])
        except:
            print(guid)
            print("ERROR: Above")

@bot.on_message_updates(filters.object_guids(admins),filters.commands("autoupdate","/"),filters.is_private,filters.is_text)
async def update_usd_price(update: Update):
    is_autoupdate=True
    await update.seen()

    while(True):
        if(is_autoupdate==False):
            break

        result = []
        # Get Prices 
        async with AsyncClient() as client:
            result = (await client.get("http://api.codebazan.ir/arz/?type=arz")).json()
            utills.aqms = (await client.get("https://aqms.doe.ir/Home/LoadAQIMap?id=2")).json()
        
        # Check Prices And Go
        if(not result["Ok"]):
            break
        result = result["Result"]
        text = """
**°**                 **💵 قیمت ارز 💵**\n
"""
        for money in result[:5]:
            text+="💵| "+ money["name"]+": "+str(money["price"])+"R\n"
        text+="\n**•**"
        await bot.edit_message(config["channel"],config["usdid"],text)
        await sleep(3600)

@bot.on_message_updates(filters.object_guids(admins),filters.commands("disautoupdate","/"),filters.is_text,filters.is_private)
async def disable_usd_update(update: Update):
    is_autoupdate = False
    await update.seen()

@bot.on_message_updates(filters.is_private,filters.object_guids(admins),filters.commands("getincome","/"),filters.is_text,filters.is_private)
async def send_income_status(update: Update):
    # Calcuting
    statusIncome["income"] = statusIncome["money"] - statusIncome["cost"]
    await update.seen()
    await update.reply(f"""
• 📊**| امار فروشگاه فرعون شاپ
**
                       
• 🚀 | کل سفارش : {await utills.stm(statusIncome["sizeorder"])}
• ✅ | موفق :     {await utills.stm(statusIncome["corder"])}
• ❌ | ناموفق :   {await utills.stm(statusIncome["norder"])}

• 🏦 | موجودی :   {await utills.stm(statusIncome["money"])}
• 💰 | سود :      {await utills.stm(statusIncome["income"])}
• 🧾 | هزینه :    {await utills.stm(statusIncome["cost"])}
""")

@bot.on_message_updates(filters.object_guids(admins),filters.commands("cleanincome","/"),filters.is_text,filters.is_private)
async def clean_status(update: Update):
    global statusIncome
    statusIncome = {
    "sizeorder":0,
    "corder":0,
    "norder":0,
    "income":0,
    "cost":79000,
    "money":0
    }
    await update.seen()

@bot.on_message_updates(filters.object_guids(admins),filters.commands("setcost","/"),filters.is_text,filters.is_private)
async def setcost(update: Update):
    statusIncome["cost"] = int(update.text.split(" ")[1])
    await update.seen()

@bot.on_message_updates(filters.object_guids(admins),filters.commands("getconfig","/"),filters.is_text,filters.is_private)
async def send_config(update: Update):
    await update.reply(utills.dumps(config))

@bot.on_message_updates(filters.object_guids(admins),filters.commands("setconfig","/"),filters.is_text,filters.is_private)
async def set_config(update: Update):
    if hasattr(update,"reply_to_message_id"):
        msgText = (await bot.get_messages_by_id(update.object_guid,[update.reply_message_id]))["messages"][0]["text"]
        config = utills.loads(msgText)
        await update.seen()

@bot.on_message_updates(filters.object_guids(admins),filters.commands("setallorder","/"),filters.is_text,filters.is_private)
async def set_all_order(update: Update):
    config["allorder"] = int(update.text.split(" ")[1])
    await update.seen()
        
# Test Robot Function
@bot.on_message_updates(filters.object_guids(admins),filters.text,filters.is_private,filters.commands("test","/"))
async def send_test_message(update: Update):
    await update.reply(f"""
    **ربات انلاین است**
    ساعت: | {utills.gettime("%H:%M:%S")}
""")

#  Help Command To Control Bot
@bot.on_message_updates(filters.object_guids(admins),filters.text,filters.is_private,filters.commands("help","/"))
async def send_help_message(update: Update):
    await update.reply("""
/test
    جهت تست کردن انلاین بودن ربات
/autoupdate
    فعال سازی بروزرسانی اتوماتیک
/disautoupdate
    لغو بروزرسانی اتوماتیک
/getincome
    گرفتن امار فروشگاه
/cleanincome
    تمیز کردن امار فروشگاه
/setcost [عدد موردنظر]
    تعیین هزینه فروشگاه
/getconfig
    گرفتن تنظیمات ربات
/setconifg [REPLY]
    تعیین تنظیمات ربات
/setallorder [عدد موردنظر]
    تعیین تمام سفارش ها
Group Management:
/gettable
گرفتن جدول
/settable [REPLY]
تعیین جدول
/joingroup link
افزودن گروه
/addbyguid
افزودن گروه با گوید
/getguidbylink
گرفتن گوید با لینک
/textall [REPLY]
فرستاند پیام به گروه ها
/forwardall [REPLY]
فوروارد به همیه گروه ها
""")

print("Bot is Running...")
bot.run()