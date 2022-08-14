from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random


end_date = os.environ['END_DATE'] # 明年冬天的日期
today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
key = os.environ['KEY']
birthday = os.environ['BIRTHDAY']
prov = os.environ['PROV']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


# 过去天数计数，相识
def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

# 生日倒计时
def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

# 目标倒计时天数
def get_over_count():
  delta_o = datetime.strptime(end_date, "%Y-%m-%d")- today
  return delta_o.days

# 调用节假日接口
def get_holiday():
    url = "http://api.tianapi.com/jiejiari/index"
    param = {'key': key,
            'date' : today
            }
    res = requests.get(url=url,params=param).json()['newslist'][0]
    today_date = res['date']    # 当前日期
    cnweekday_date = res['cnweekday']   # 当前星期
    holiday_date = res['name']   # 当前节假日
    if res['isnotwork'] == 1:
        string_data = '难得的假期，好好休息吧！'
    else:
        string_data = '今天也要努力工作哦！'
    return today_date,cnweekday_date,holiday_date,string_data



# 调用天气预报
def get_weather_forecast():
    url = 'http://api.tianapi.com/tianqi/index'
    param = {'key':key,
             'city':city
            }
    res = requests.get(url=url,params=param).json()['newslist'][0]
    location = res['area']
    weather_data = res['weather']
    now_temperature = res['real']
    low_temperature = res['lowest']
    high_temperature = res['highest']
    warm_tips = res['tips']
    return location,weather_data,now_temperature,low_temperature,high_temperature,warm_tips

# 调用实时油价接口
def get_oil_price():
    url = 'http://api.tianapi.com/oilprice/index'
    param = {'key': key,
             'prov': prov
             }
    res = requests.get(url=url, params=param).json()['newslist'][0]
    p92 = res['p92']
    p95 = res['p95']
    return p92,p95


def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

def get_rainbow_words():
  url = "http://api.tianapi.com/caihongpi/index?key=" + key
  res = requests.get(url).json()['newslist'][0]
  return res['content']


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
today_date,cnweekday_date,holiday_date,string_data = get_holiday()
location,weather_data,now_temperature,low_temperature,high_temperature,warm_tips = get_weather_forecast()
p92,p95 = get_oil_price()
data = {"today_date":{"value":today_date},
        "cnweekday_date":{"value":cnweekday_date},
        "holiday_date":{"value":holiday_date},
        "string_data":{"value":string_data},
        "location":{"value":location},
        "weather_data":{"value":weather_data,"color":get_random_color()},
        "now_temperature":{"value":now_temperature,"color":get_random_color()},
        "low_temperature":{"value":low_temperature,"color":get_random_color()},
        "high_temperature":{"value":high_temperature,"color":get_random_color()},
        "warm_tips":{"value":warm_tips,"color":get_random_color()},
        "p92":{"value":p92,"color":get_random_color()},
        "p95":{"value":p95,"color":get_random_color()},
        "birthday":{"value":get_birthday(),"color":get_random_color()},
        "start_days":{"value":get_count(),"color":get_random_color()},
        "over_days":{"value":get_over_count(),"color":get_random_color()},   
        "rainbow_words":{"value":get_rainbow_words(), "color":get_random_color()}
       }
res = wm.send_template(user_id, template_id, data)
print(res)
