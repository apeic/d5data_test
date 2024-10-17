import json
import time
import requests
import random
from tqdm import tqdm
import pymysql

PARAMS = {
    'deviceId': 'C3547E73-0A58-418B-91FA-766CFD49F613',
    'dist': 'appstore',
    'model': 'iPad8,6',
    'os_version': '16.1',
    'platform': '2',
    'secondsFromGMT': '28800',
    'smDeviceId': '202305062207595edf57dcdbfb9309025ee4c283160485008b95c0cd0af5da',
    'version': '3.14.6',
    'x-jike-device-properties': '{"idfv":"00000000-0000-0000-0000-000000000000","idfa":"D02856C2-1D25-45B6-BE65-0069EE3DA93E"}'
}

headers = {
    'authority': 'api.jijigugu.club',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Microsoft Edge";v="96"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'ygt': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOjg5MjY1MzYsImV4cCI6MTcyODgyNDMyMH0.0ZTSqJLuZfK6uGad2-nm8iUNEyBczKq2uOGTx2wqkJg'
}

DIARY_TYPE = {'4Jq3YdoNyG9pzw5MxPQ0': '丧',
 'R68LbZPMpA3yDYeNdOax': '恋爱',
 'Ar0Kkz1epbNp8JoG2j9V': '吐槽',
 'QMwOWz6ayxJpGAbDxoLq': '秘密',
 'KJ3ZdGzryM07W8eB9RQ1': '孤独',
 '4zqO9wx5ErbELV3gjePD': '开心',
 '5X0nze817jGyamVNrbBD': '烦恼',
 '5Dolk0XK75A7j41NJ2re': '抑郁',
 'BAglDvmoEL3yP3M1baqK': '暗恋',
 '14zZQn8Gyq479JWRVBem': '前任',
 'bmgzAjX3p8Xopw5W1eBo': '柠檬精',
 'Rgjb3WM6yVOEZomN912v': '自言自语',
 '14zZQn8GyqX479JWRVBe': '沙雕',
 'Db2moNRgpB2pQ4YrOW9w': '求撩',
 'V3vgDL5ZEZqyYXqQb9Ge': '找同好',
 'evwB0oDG7Rjr739axJQ8': '头像',
 'evwB0oDG7Rr739axJQ8n': '自拍',
 '2MAKYgN8yDdyJVWaqrnv': '求助',
 'PWzkJvgRp967VYmbGMXw': '好奇',
 'Db2moNRgpBb2pQ4YrOW9': '声控',
 'AwYqJePky6RryQb5Gdnm': '壁纸',
 'KJ3ZdGzryMo0pW8eB9RQ': '表情包',
 'dVDRk4XqE3qj7NnaK6M3': '投票',
 'nVe9Q8G6yebEk5gZYxOm': '学习',
 'R68LbZPMpAb37DYeNdOa': '脑洞',
 'AwYqJePky6ryQb5GdnmW': '安利',
 'RYPe5N1WEORynlA3KZJg': '治愈',
 'XDPWKv357WaAErB6OQgm': '游戏',
 'zM92vXompvlyxjkYb5rd': '句子',
 '3MzxjqNby24dpr06gKnO': '读书',
 'QMwOWz6ayxaJEGAbDxoL': '追剧',
 'WQ5rzYx2ykdEO6X4w0V3': '爱豆',
 'Rgjb3WM6yVROyZomN912': '二次元',
 'QYDRZMmvpY5plWJwx6d8': '摄影',
 'Xw9YdJb3pwx78zMrlqQ0': '电影',
 'BvZK4XrxpobE213LnjaP': '音乐',
 '2MAKYgN8yDPdyJVWaqrn': '绘画',
 '6XaWOd817KBNpN2RnQYj': '纸条',
 'N3ZOwLQXplgEdW82v0Bn': '此刻',
 'V3vgDL5ZEZ9qyYXqQb9G': '校园',
 'aW96gBj2pnJpkl4N310G': '美食',
 'aJ9VNeGvpJ4ygMYxd4Db': '心愿',
 'ORgm3bzX7a3E1kKV0xev': '梦',
 'erNl1nqbE0AZpLwmdvV2': '职场',
 'kLAPKD2q7g1NEjmvM8lX': '海外',
 'kLAPKD2q7gNpjmvM8lXo': '一罐反馈'}

base_url = 'https://api.jijigugu.club'

def get_params(path, **kwargs):
    params = {}
    for k, v in kwargs.items():
        k = ''.join([k.split('_')[0], *[_.title() for _ in k.split('_')[1: ]]])
        params[k] = v
    return {
        'path': path,
        'params': params
    }

def write_to_json(file: str, new_data: list):
    try:
        with open(file, 'r') as fp:
            data = json.load(fp)
    except:
        data = []
    data.extend(new_data)
    print(f'正在保存{len(new_data)}条数据...')
    with open(file, 'w') as fp:
        json.dump(data, fp, ensure_ascii=False)

def send_request(p, method='get'):
    url = base_url + p['path']
    params = PARAMS.copy()
    params.update(p['params'])
    if method == 'get':
        r = requests.get(url, headers=headers, params=params)
    elif method == 'post':
        r = requests.post(url, headers=headers, data=params)
    t = json.loads(r.text)
    return t


def get_ip_location(dairy_id):
    params = get_params('/diary/detail', id=dairy_id)
    return send_request(params)['data']['ipLocation']
 

def get_new_diary(mid):
            
    def insert_user(user_id):
        sql = 'insert ignore into user(id, avatar, des, city, constellation, nickname, gender, birthday, followNum, followedNum, ipLocation) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        params = get_params('/realProfile/get', id=user_id)
        data = send_request(params)['data']
        data['desc'] = str(data['desc'])
        data['avatar'] = data['avatar']['key']
        cursor.execute(sql, list(map(data.get, 'id, avatar, desc, city, constellation, nickname, gender, birthday, followNum, followedNum, ipLocation'.split(', '))))
        db.commit()
        
    db = pymysql.connect(host='127.0.0.1',
                     user='one',
                     password='one',
                     database='one',
                     charset='utf8mb4')

    cursor = db.cursor()
    
    sql = 'insert ignore into diary(id, age, createTime, gender, commentedNum, isLiked, likedNum, nickname, photos, text, isReal, userId, mid, ipLocation) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(f'select createTime from diary where mid = "{mid}" ORDER BY createTime desc limit 1')
    last = cursor.fetchone()[0]
    
    last_score = None
    flag = True

    while flag:
        try:
            params = get_params('/feed/list', mid=mid, last_score=last_score)
            data = send_request(params)['data']
        except:
            break
        last_score = data[-1]['id']
        for d in data:
            if d['createTime'] < last:
                flag = False
                break
            d['userId'] = d['user'].pop('id', None)
            d.update(d['user'])
            del d['user']
            info = list(map(d.get, 'id, age, createTime, gender, commentedNum, isLiked, likedNum, nickname, photos, text, isReal, userId'.split(', ')))
            info[8] = str(info[8])
            info.append(d['mood']['id'])
            info.append(get_ip_location(info[0]))
            s = cursor.execute(sql, info)
            db.commit()
            if d['isReal']:
                insert_user(d['userId'])
            # print(d['id'])






        


        
