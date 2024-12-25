from json import dumps,loads,load
from time import strftime as gettime
from time import time
from random import randint


insuits = load(open("insuits.json",'r'))
admins = {}
last_update = 0

async def stm(price: int):
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
  
async def has_link(text: str):
    if "https://" in text or "http://" in text or "@" in text or ".com" in text:
        return True
    return False

async def has_insuit(text: str):
    global insuits
    for insuit in insuits:
        if insuit in text.replace(".","").replace("#","").replace("-","").lower():
            return True
    return False

speak = load(open("speak.json","r"))
aqms = []