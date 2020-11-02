import websocket
import re
from datetime import datetime
import time
import pymongo
n=input('请输入房间号:')
print('有啥需要改进的记得留言到847262823@qq.com,感谢帅哥美女们的支持，前方高能预警，一大波弹幕来袭')
a = 0
b = 0
starttime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
start=time.time()
print(starttime)
Client=pymongo.MongoClient(host='localhost',port=27017)
db=Client['弹幕']
collections=db['弹幕']
def on_open(ws):
    print('open')
    login(ws)
    joingroup(ws)
def on_error(ws):
    print('error')
def handel_message(msg):
    data_len=len(msg)+9
    data_type=msg.encode('utf-8')
    head=int.to_bytes(data_len,4,'little')
    #689
    info_type=bytearray([0xb1, 0x02, 0x00, 0x00])
    end=bytearray([0x00])
    data=head+head+info_type+data_type+end
    return data
def login(ws):
    msg=f'type@=loginreq/roomid@={n}/'.format(n)
    hah=handel_message(msg)
    ws.send(hah)
def joingroup(ws):
    msg=f'type@=joingroup/rid@={n}/gid@=-9999/'.format(n)
    rile=handel_message(msg)
    ws.send(rile)
def savetomongo(content):
    collections.insert_one(content)
def savelocal(content):
    with open('./douyudanmu.txt','a') as f:
        f.write(content+'\n')
        f.close()
def keeplive(ws):
    msg = 'type@=keeplive/tick@=' + str(int(time.time())) + '/'
    caole = handel_message(msg)
    ws.send(caole)
def on_message(ws,message):
    global a,b,starttime,start,end
    html=message.decode(encoding='utf-8',errors='ignore')
    pattern=re.compile('nn@=(.*?)/.*?txt@=(.*?)/.*?level@=(.*?)/.*?bnn@=(.*?)/',re.S)
    content=re.findall(pattern,html)
    for item in content:
        if len(item[3])>0:
            end = time.time()
            danmu=datetime.now().strftime('%Y-%m-%d %H:%M:%S') + f'(徽章){item[3]} (等级){item[2]} (用户){item[0]} (弹幕):{item[1]}'.format(item)
            print(danmu)
            savelocal(danmu)
            zuilea= {
                '徽章':item[3],
                '等级':item[2],
                '昵称':item[0],
                '弹幕':item[1]
            }
            savetomongo(zuilea)
        else:
            danmu=datetime.now().strftime('%Y-%m-%d %H:%M:%S') +f'(等级){item[2]} (用户){item[0]} (弹幕):{item[1]}'.format(item)
            print(danmu)
            zuilea = {
                '徽章': '送礼不存在的，白嫖',
                '等级': item[2],
                '昵称': item[0],
                '弹幕': item[1]
            }
            savetomongo(zuilea)
    if int(end) - int(start) > 100:
        #print('发送一次心跳消息给服务器，证明我们在，不会浪费资源')
        keeplive(ws)
        start = end
def on_close(ws):
    print('close')
def main():
    ws=websocket.WebSocketApp('wss://danmuproxy.douyu.com:8502/'
                              ,on_open=on_open, on_message=on_message, on_error=on_error,on_close=on_close)
    ws.run_forever()
if __name__=='__main__':
    main()