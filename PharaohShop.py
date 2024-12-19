from rubpy import Client,filters # pip3 install rubpy
from rubpy.types import Update # pip3 install rubpy
from requests import get # pip3 install requests
import asyncio
from json import dumps,loads
from os import remove
import aiohttp # pip3 install aiohttp
from aiofile import async_open as open# pip3 install aiofile
from time import strftime

# Config The Bots Variables
admins = ["u0DsXjn0fe84d636cf1f42a0cb292693","u0DwuqS017f68d4545e326e0bbcd9ca6"]
config = {
    "channel":"c0CPOlg02db41ed2e478961d720f330f",
    "usdid":"1093267119967785",
    "prdsave":"c0CPlFv09746422e4b7f4861036a3e29",
    "allorder":100,
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

bot = Client("account.rp")
is_autoupdate = False
# Functions Bot Use Them 
async def download_file(url,output):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            async with open(output,"wb") as handle:
                async for chunk in res.content.iter_chunked(1024*1024*100):
                    await handle.write(chunk)
# Need Optimizing 
def stm(price: int):
    result=""
    pstr = str(price)
    i=0
    pos=0
    for c in pstr[::-1]:
        pos+=1
        result+=c
        if c=="-":
            continue
        i+=1
        if i==3 and (not len(pstr)==pos or not 0==pos):
            result+=','
            i=0
    return result[::-1]

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



# Admin Commands
@bot.on_message_updates(filters.object_guids(admins),filters.commands("autoupdate","/"),filters.is_private,filters.is_text)
async def update_usd_price(update: Update):
    is_autoupdate=True
    await update.seen()

    while(True):
        if(is_autoupdate==False):
            break

        result = []
        # Get Prices 
        async with aiohttp.ClientSession() as session:
            async with session.get("http://api.codebazan.ir/arz/?type=arz") as res:
                result = await res.json()
        
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
        await asyncio.sleep(5)

@bot.on_message_updates(filters.object_guids(admins),filters.commands("disautoupdate","/"),filters.is_text,filters.is_private)
async def disable_usd_update(update: Update):
    is_autoupdate = False
    await update.seen()

@bot.on_message_updates(filters.object_guids(admins),filters.commands("msgid","/"),filters.is_text,filters.is_private)
async def get_message_id(update: Update):
    #NEED
    print(await bot.get_messages_by_id(config["channel"],config["usdid"]))

@bot.on_message_updates(filters.is_private,filters.object_guids(admins),filters.commands("getincome","/"),filters.is_text,filters.is_private)
async def send_income_status(update: Update):
    # Calcuting
    statusIncome["income"] = statusIncome["money"] - statusIncome["cost"]
    await update.seen()
    await update.reply(f"""
• 📊**| امار فروشگاه فرعون شاپ
**
                       
• 🚀 | کل سفارش : {stm(statusIncome["sizeorder"])}
• ✅ | موفق :     {stm(statusIncome["corder"])}
• ❌ | ناموفق :   {stm(statusIncome["norder"])}

• 🏦 | موجودی :   {stm(statusIncome["money"])}
• 💰 | سود :      {stm(statusIncome["income"])}
• 🧾 | هزینه :    {stm(statusIncome["cost"])}
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
    print(update.text.split(" ")[1])
    print(int(update.text.split(" ")[1]))
    await update.seen()

@bot.on_message_updates(filters.object_guids(admins),filters.commands("getconfig","/"),filters.is_text,filters.is_private)
async def send_config(update: Update):
    await update.reply(dumps(config))

@bot.on_message_updates(filters.object_guids(admins),filters.commands("setconfig","/"),filters.is_text,filters.is_private)
async def send_config(update: Update):
    if hasattr(update,"reply_to_message_id"):
        msgText = (await bot.get_messages_by_id(update.object_guid,[update.reply_message_id]))["messages"][0]["text"]
        config = loads(msgText)
        await update.seen()

@bot.on_message_updates(filters.object_guids(admins),filters.commands("setallorder","/"),filters.is_text,filters.is_private)
async def send_config(update: Update):
    config["allorder"] = int(update.text.split(" ")[1])
    await update.seen()

@bot.on_message_updates(filters.object_guids(admins),filters.commands("uploadvideo","/"),filters.is_text,filters.is_private)
async def upload_video_channel(update: Update):
    params = update.text.split("\n")
    url = params[1]
    hashtag = params[2]
    caption = params[3]

    # First Download File
    await update.reply("فایل شما درحال دانلود شدن است")
    await download_file(url,"file.mp4")
    
    # Upload
    await update.reply("فایل شما در حال اپلود است")
    await bot.send_video(config["upload"],"file.mp4",f"""•
  🎬| #ویدیو {hashtag}
  🧾| توضیحات:  {caption}
  
💎| • تماشا با کیفیت بالا •

    بکوب روی جوین یا پیوستن
  **•√Pharaoh√Shop• فرعون شاپ**
  @pharaohshop
°
""")
    await update.reply("فایل شما اپلود شد.")
    remove("file.mp4")
        
# Test Robot Function
@bot.on_message_updates(filters.object_guids(admins),filters.text,filters.is_private,filters.commands("test","/"))
async def send_test_message(update: Update):
    await update.reply(f"""
    **ربات انلاین است**
    ساعت: | {strftime("%H:%M:%S")}
""")
@bot.on_message_updates(filters.object_guids(admins),filters.text,filters.is_private,filters.commands("channel","/"))
async def get_channel_info(update: Update):
    members = []
    mem = (await bot.get_channel_all_members(config["channel"]))["in_chat_members"]
    for member in mem:
        members.append(member["member_guid"])
    await update.reply(str(members))

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
/uploadvideo [:url] [:hashtag] [:caption]
    اپلود کردن ویدیو
""")

bot.run()