from faker import Faker
import random
import MySQLdb

faker = Faker(locale='zh_CN')

db = MySQLdb.connect("localhost", "root", "123456", "musesart", charset='utf8')
cursor = db.cursor()

id = 1
for i in range(3, 100):
    sql = "SELECT nickname from user WHERE user.id="+str(i)
    cursor.execute(sql)
    nickname = cursor.fetchone()[0]

    for j in range(4):
        sql = "INSERT INTO address (id, add_time, address, city, district, province, signer_mobile, signer_name, user_id) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

        cursor.execute(sql, [id, faker.date_between(start_date='-60d', end_date='-10d'), faker.street_address(), faker.city_name()+"市",
                             faker.district()+"区", faker.province(), faker.phone_number(), nickname, i])
        db.commit()
        id += 1
    print(i)


