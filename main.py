import os
import ccxt
import time
import discord
import json
from replit import db
import keep_alive
import datetime

"""print("ปี : %d" % now.year)
print("เดือน : %d" % now.month)
print("วันที่ : %d" % now.day)
print("ชั่งโมง : %d" % now.hour)
print("นาที : %d" % now.minute)
print("วินาที : %d" % now.second)"""
"""print("ไมโครวินาที : %d" % now.microsecond)"""




class Client(discord.Client):

    async def on_ready(self):
        print('Login done!', self.user)

    async def on_message(self, message):
      
        # ADA_info = bn.fetch_tickers('ADA/BUSD')

        if message.author == self.user:
            return
        
        if message.content == "create_room":
          channel = await message.guild.create_text_channel("มาเทรดกาน", )

          db["textCh"] = channel.id

          return


        if db["textCh"] != 0 and message.content == "ดูราคาADA":
          # ADA = ADA_info['ADA/BUSD']['last']
          # await message.channel.send(ADA)
          return

    

def Rebalance(t,b,bn):

  ADA_info = bn.fetch_tickers('ADA/BUSD')
  Balance = bn.fetchBalance()

  ADA = ADA_info['ADA/BUSD']['last']  # ราคา ADA ต่อ BUSD
  ADA_V = Balance['ADA']['free']  # จำนวน ADA ที่มี
  V_ADA = ADA * ADA_V  # จำนวน ADA ต่อ BUSD ที่มี $

  BUSD_V = Balance['BUSD']['free']

  if V_ADA > t:  # V >= 82 - 1
    orderSell = (10/ADA)+0.13
    bn.create_market_sell_order('ADA/BUSD',orderSell)
    print(f"SELL ADA @Marketprice {orderSell}$")
    print(f"ราคา ADA = {ADA}")
    print(f"จำนวน ADA ที่มี = {ADA_V}")
    print(f"ADA รวมแล้วมี {V_ADA} ~$")
    print(f"BUSD รวมแล้วมี {BUSD_V} ~$")
    print("เวลา GMT +7")
    print("เดือน : %d" % now.month)
    print("วันที่ : %d" % now.day)
    print("ชั่งโมง : %d" % now.hour)
    print("นาที : %d" % now.minute)
    print("วินาที : %d" % now.second)
    time.sleep(2)
  
  elif V_ADA < b:  # V <= 68 + 1
    orderBuy = (10/ADA)+0.13
    bn.create_market_buy_order('ADA/BUSD',orderBuy)
    print(f"BUY ADA @Marketprice {orderBuy}$")
    print(f"ราคา ADA = {ADA}")
    print(f"จำนวน ADA ที่มี = {ADA_V}")
    print(f"ADA รวมแล้วมี {V_ADA} ~$")
    print(f"BUSD รวมแล้วมี {BUSD_V} ~$")
    print("เวลา GMT +7")
    print("เดือน : %d" % now.month)
    print("วันที่ : %d" % now.day)
    print("ชั่งโมง : %d" % now.hour)
    print("นาที : %d" % now.minute)
    print("วินาที : %d" % now.second)
    time.sleep(2)

  else:
    print("นั่งทับมือ")
    print("เวลา GMT +7")
    print("เดือน : %d" % now.month)
    print("วันที่ : %d" % now.day)
    print("ชั่งโมง : %d" % now.hour)
    print("นาที : %d" % now.minute)
    print("วินาที : %d" % now.second)


def run():
  Token = os.environ['TOKEN']
  if Token:
      Client().run(Token)
  else:
      print("Looks like you're not the owner")


keep_alive.keep_alive()

file = open('config.json')
config = json.load(file)
fix = int(config['fix']) # 75
fee = int(config['rebal']) # 7
top = (fix+fee) - 1  # 82 (-1)
bottom = (fix-fee) + 1  # 68 (+1)

my_API = os.environ['API']
my_secret = os.environ['Secret']
  

bn = ccxt.binance({
  'api_key': my_API,  # API Keys
  'secret': my_secret,  # API Secret
  'enableRateLimit': True,
})

while 1:
  now = datetime.datetime.now()
  print("Start Rebalance")
  Rebalance(top,bottom,bn)
  print("\n")
  time.sleep(2)