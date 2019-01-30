import requests
import json
import MySQLdb
import random
from faker import Faker
faker = Faker(locale='zh_CN')
db = MySQLdb.connect("localhost", "root", "123456", "musesart", charset='utf8')
cursor = db.cursor()

for i in range(4,21):
    for j in range(1,3+1):
        print(i,j)
        f = open("json_"+str(i)+"_"+str(j)+".json", encoding="utf-8")
        texts = f.read().replace("👍","").replace("🏻","").replace("💐","").\
            replace("🔥","").replace("😜","").replace("😬","").replace("😀","")\
            .replace("🌹","").replace("😘","").replace("😊","").split("<tr>")
        comments = []
        for text in texts:
            dic = {}
            try:
                content = text.split('<div class="tm-rate-fulltxt">')[1].split("</div>")[0]
                images = []
                temps = text.split("img src")#[1].split(">")[0][2:-1].split("_40x40.jpg")[0]
                for temp in temps:
                    if temp.startswith('="//'):
                        image = temp.split(">")[0][2:-1].split("_40x40.jpg")[0]
                        if image != "":
                            image = "http:"+image
                        images.append(image)
                brief = text.split('p title="')[1].split('"')[0]
                print(brief)
                dic["content"] = content
                dic["photos"] = images
                dic["brief"] = brief
                comments.append(dic)
            except:pass

        for comment in comments:
            print(comment)

            """第一步：加载淘宝评论的内容和图片"""
            photos = comment["photos"]
            content = comment["content"]


            """第二步：查询商品信息"""
            SQL = "SELECT * from commodity WHERE id="+str(i)
            cursor.execute(SQL)
            result = cursor.fetchone()
            number = random.randint(1,5)
            commodity_id = result[0]
            discount_price = result[8]

            user_id = random.randint(3,99)
            """第三步：选择商品属性与参数"""
            brief = comment["brief"]

            """第四步：查询用户的地址"""
            SQL = "SELECT * from address WHERE user_id="+str(user_id)
            cursor.execute(SQL)
            results = cursor.fetchall()
            if len(results) == 1:
                result = results[0]
            else:
                result = results[random.randint(0, len(results)-1)]
            address = result[5]+result[3]+result[4]+result[2]

            """第五步：创建订单"""
            SQL = "INSERT INTO torder (order_amount, order_sn, pay_status, pay_time, trade_no, address, user_id) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s)"
            time_ = faker.date_between(start_date='-20d')
            cursor.execute(SQL, [discount_price*number, faker.uuid4(), 1, time_,
                                 faker.uuid4(), address, user_id])
            db.commit()
            sql = "SELECT LAST_INSERT_ID()"
            cursor.execute(sql)
            order_id = cursor.fetchone()[0]

            """第六步：复制商品信息"""
            SQL = "INSERT INTO order_commodity (add_time, brief, commodity_id, `number`, order_id, price) " \
                  "VALUES (%s, %s, %s, %s, %s, %s)"

            cursor.execute(SQL, [time_, brief, commodity_id, number, order_id, discount_price*number])
            db.commit()
            sql = "SELECT LAST_INSERT_ID()"
            cursor.execute(sql)
            order_commodity_id = cursor.fetchone()[0]

            """第七步：添加评论"""
            print(content)
            SQL = "INSERT INTO comment (add_time, comment, commodity_id, order_commodity_id, order_id, user_id)" \
                  " VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(SQL, [time_, content, commodity_id, order_commodity_id, order_id, user_id])
            db.commit()
            sql = "SELECT LAST_INSERT_ID()"
            cursor.execute(sql)
            comment_id = cursor.fetchone()[0]

            """第八步：添加评论图片"""
            for image_url in photos:
                SQL = "INSERT INTO image (comment_id, image_url) VALUES (%s, %s)"
                cursor.execute(SQL, [comment_id, image_url])
                db.commit()

