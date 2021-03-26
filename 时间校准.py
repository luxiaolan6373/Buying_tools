import requests,time,os,sys


def get_beijing_time(typ='0',):
    #记下时间
    start_time = int(round(time.time() * 1000))
    if typ=='0':#北京时间
        url='http://www.daojishiqi.com/sj.asp'
        res = requests.get(url)
    elif typ=='1':#京东时间
        url = 'https://a.jd.com//ajax/queryServerData.html'
        res = requests.get(url)
        res.text=res.text.split('"serverTime":')[-1].split('}')[0]
    elif typ=='2':#淘宝时间
        url = 'http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp'
        res = requests.get(url)
        res.text=res.text.split('{"t":"')[-1].split('"}}')[0]
    sc_time=int(round(time.time() * 1000)) - start_time
    # 这个sc_time*3.5   可以自己改成任意的误差,,自己根据情况来改想办法改到最合适,目前这个在我电脑上误差几乎为0
    now_time = time.localtime((int(res.text) + sc_time * 3.5) / 1000)
    os.system("time %02u:%02u:%02u" % (now_time.tm_hour, now_time.tm_min, now_time.tm_sec))
    #修改成功
    input('修改成功!按任意键退出!')
key=input('请选择在线时间服务器: \n0.北京时间\n1.京东时间\n2.淘宝时间\n')
try:
    get_beijing_time(key)
except:
    get_beijing_time()
