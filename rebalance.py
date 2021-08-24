import os
import ccxt
import time
import json
import datetime



def running():
  now = datetime.datetime.now()
  file = open('config.json')
  config = json.load(file)
  fix = int(config['fix']) # 75
  fee = int(config['rebal']) # 7
  top = (fix+fee) - 1  # 82 (-1) = 81
  bottom = (fix-fee) + 1  # 68 (+1) = 69

  my_API = os.environ['API']
  my_secret = os.environ['Secret']
  


  bn = ccxt.binance({
    'api_key': my_API,  # API Keys
    'secret': my_secret,  # API Secret
    'enableRateLimit': True,
  })

  ADA_info = bn.fetch_tickers('ADA/BUSD')
  Balance = bn.fetchBalance()

  ADA = ADA_info['ADA/BUSD']['last']  # ราคา ADA ต่อ BUSD ล่าสุด  
  ADA_V = Balance['ADA']['free']  # จำนวน ADA ที่มีในกระเป๋า     
  V_ADA = ADA * ADA_V  # จำนวน ADA ต่อ BUSD ที่มี $   
  BUSD_V = Balance['BUSD']['free']

  s,h,m,d,mth = now.second,now.hour,now.minute,now.day,now.month

  t,b = top,bottom
  GMT = 7
  temp = (h+GMT) // 24
  h += GMT
  if h > 24:
    h -= 24
  else:
    pass
  d += temp
  if V_ADA > t:  # V > 82 - 1
    orderSell = (10/ADA)+0.13
    bn.create_market_sell_order('ADA/BUSD',orderSell)
    print(f"SELL ADA @Marketprice {orderSell}$")
    print(f"ราคา ADA = {ADA}")
    print(f"จำนวน ADA ที่มี = {ADA_V}")
    print(f"ADA รวมแล้วมี {V_ADA} ~$")
    print(f"BUSD รวมแล้วมี {BUSD_V} ~$")
    print(f"วันเวลา {h}:{m}:{s} วันที่ {d} เดือน {mth}")
    print("\r")
    time.sleep(2)
  
  elif V_ADA < b:  # V < 68 + 1
    orderBuy = (10/ADA)+0.13
    bn.create_market_buy_order('ADA/BUSD',orderBuy)
    print(f"BUY ADA @Marketprice {orderBuy}$")
    print(f"ราคา ADA = {ADA}")
    print(f"จำนวน ADA ที่มี = {ADA_V}")
    print(f"ADA รวมแล้วมี {V_ADA} ~$")
    print(f"BUSD รวมแล้วมี {BUSD_V} ~$")
    print(f"วันเวลา {h}:{m}:{s} วันที่ {d} เดือน {mth}")
    print("\r")
    time.sleep(2)
  else:
    print("นั่งทับมือ")
    print(f"ราคา ADA = {ADA}")
    print(f"ADA รวมแล้วมี {V_ADA} ~$")
    print(f"วันเวลา {h}:{m}:{s} วันที่ {d} เดือน {mth}")
    print("\r")
