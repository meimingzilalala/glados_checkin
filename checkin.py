import json,os
# server酱开关，填off不开启(默认)，填on同时开启cookie失效通知和签到成功通知
sever = os.environ["SERVE"]
# 填写server酱sckey,不开启server酱则不用填
sckey = os.environ["SCKEY"]
#'SCU89402Tf98b7f01ca3394b9ce9aa5e2ed1abbae5e6ca42796bb9'
# 填入glados账号对应cookie
cookie = os.environ["COOKIE"]
#'__cfduid=d3459ec306384ca67a65170f8e2a5bd561593049467; _ga=GA1.2.766373509.1593049472; _gid=GA1.2.1338236108.1593049472; koa:sess=eyJ1c2VySWQiOjQxODMwLCJfZXhwaXJlIjoxNjE4OTY5NTI4MzY4LCJfbWF4QWdlIjoyNTkyMDAwMDAwMH0=; koa:sess.sig=6qG8SyMh_5KpSB6LBc9yRviaPvI'
from curl_cffi import requests

def start():
    
    url= "https://glados.network/api/user/checkin"
    url2= "https://glados.network/api/user/status"
    referer = 'https://glados.network/console/checkin'
    myHeaders = {
        "cookie": cookie,
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://glados.network",
        "referer": "https://glados.network/console/checkin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
    }
    # checkin = requests.post(url,headers={'cookie': cookie ,'referer': referer },data={"token": "glados.one" })
    # checkin = requests.post(url,headers=myHeaders,data={"token": "glados.network" })
    # 使用 impersonate 参数指定要模拟的浏览器
    session = requests.Session()
    # 模拟 Chrome 的 TLS 指纹
    checkin = requests.post(
        url,
        headers=myHeaders,
        data='{"token": "glados.network"}',
        impersonate="chrome131",  # 与 UA 中的版本一致
    )
    print(checkin.json())
    state =  requests.get(url2,headers=myHeaders)

    if 'message' in checkin.text:
        mess = checkin.json()['message']
        time = state.json()['data']['leftDays']
        time = time.split('.')[0]
        print(time)
        
        if sever == 'on':
            requests.get('https://sctapi.ftqq.com/' + sckey + '.send?text='+mess+'，' + time)
    else:
        requests.get('https://sctapi.ftqq.com/' + sckey + '.send?text=cookie过期')

def main_handler(event, context):
  return start()

if __name__ == '__main__':
    start()






