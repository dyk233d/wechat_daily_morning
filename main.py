from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
call_back_id = os.environ["CALL_BACK_ID"]
template_id = os.environ["TEMPLATE_ID"]
tianxin_apikey = os.environ["APIKEY"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  str1 = '天气：' + str(weather["weather"])+'\n当前气温：'+ str(weather["temp"]) \
          +'\n最低气温：'+str(weather["low"])+'\n最高气温：'+str(weather["high"]) \
          +'\n风向：'+str(weather["wind"]) +'\n空气质量：' + str(weather["airQuality"]) +'\n湿度：' + str(weather["humidity"])
  return str1

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  #words = requests.get("https://api.shadiao.pro/chp")   #这个能用
  param = {'key': tianxin_apikey}
  words = requests.post("https://apis.tianapi.com/healthtip/index",params = param)
  if words.status_code != 200:
    return get_words()
  return words.json()['result']['content']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea = get_weather()
data = {"date":{"value":str(today)[:10], "color":get_random_color()},"city":{"value":city, "color":get_random_color()},"weather":{"value":wea},"love_days":{"value":get_count(), "color":get_random_color()},"birthday_left":{"value":get_birthday(), "color":get_random_color()},"words":{"value":get_words(), "color":get_random_color()}}
#res = wm.send_template(user_id, template_id, data)
#print(res)
res = wm.send_template(call_back_id, template_id, data)
print(res)
