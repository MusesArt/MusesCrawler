from faker import Faker
import random
import MySQLdb

faker = Faker(locale='zh_CN')

db = MySQLdb.connect("localhost", "root", "123456", "musesart", charset='utf8')
cursor = db.cursor()


for i in range(3, 100):
    commodityId = random.randint(1, 20)
    SQL = "SELECT id, `name` from attribute WHERE commodity_id="+str(commodityId)
    cursor.execute(SQL)
    ids = cursor.fetchall()
    info = ""
    for id, name in ids:
        SQL = "SELECT value, image from parameter WHERE attribute_id="+str(id)
        cursor.execute(SQL)
        res = cursor.fetchall()
        value = res[random.randint(0, len(res)-1)]
        info += name+":"+value[0]+";"
    SQL = "INSERT INTO cart(add_time, commodity_id, number, user_id, detail, image) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(SQL, [faker.date_between(start_date='-90d', end_date='-10d'), commodityId, random.randint(1,10),
                         i, info, value[1]])
    db.commit()
    print(i)



