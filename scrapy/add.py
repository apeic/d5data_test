from utils import *

def get_new_diary(name, mid):
            
    def insert_user(user_id):
        sql = 'insert ignore into user(id, avatar, des, city, constellation, nickname, gender, birthday, followNum, followedNum, ipLocation) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        params = get_params('/realProfile/get', id=user_id)
        try:
            data = send_request(params)['data']
        except:
            return
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
    last = cursor.fetchone()
    if last is None:
        return
    last = last[0]
    # last = 1719763200
    last_score = None
    flag = True
    err_cnt = 0
    cnt = 0

    while flag:
        try:
            params = get_params('/feed/list', mid=mid, last_score=last_score)
            data = send_request(params)['data']
        except:
            err_cnt += 1
            if err_cnt < 5:
                continue
            else:
                with open('err.log', 'a') as fp:
                    fp.write(f'{mid} {last_score}\n')
                break
        if len(data) == 0:
            break
        last_score = data[-1]['score']
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
        cnt += 1
        print(name, cnt)

res = requests.get('https://api.jijigugu.club/mood/listAll/V2?deviceId=B2F32DBD-ED83-4F76-90D1-CA28CCFC3E8F&dist=appstore&model=iPhone15%2C3&os_version=16.2&platform=2&secondsFromGMT=28800&smDeviceId=2020041413581993b4e50e64f7977820c1aa093bfa6e3a01412c7364e0a2c0&version=3.14.6&x-jike-device-properties=%7B%22idfa%22%3A%2200000000-0000-0000-0000-000000000000%22%2C%22idfv%22%3A%225367ABA6-DB5F-4A93-A578-1AC84781784C%22%7D')
data = json.loads(res.text)
x = {}
for d in data['data'][2]['listAll']:
    for l in d.get('list'):
        x[l['name']] = l['id']
for name, mid in x.items():
    get_new_diary(name, mid)        
