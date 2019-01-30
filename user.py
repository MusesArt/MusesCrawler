from faker import Faker
import random
import MySQLdb

faker = Faker(locale='zh_CN')

db = MySQLdb.connect("localhost", "root", "123456", "musesart", charset='utf8')
cursor = db.cursor()

avatars = ["https://s1.ax1x.com/2018/06/22/PpBIIJ.jpg",
            "https://s1.ax1x.com/2018/06/22/Ppyv6I.jpg",
            "https://s1.ax1x.com/2018/06/22/Pp6978.jpg",
            "https://s1.ax1x.com/2018/06/22/Ppyv6I.jpg",
            "https://s1.ax1x.com/2018/06/22/PpyFQ1.jpg",
            "https://s1.ax1x.com/2018/06/22/PpBWrT.jpg",
            "https://s1.ax1x.com/2018/06/22/PpsIIg.jpg",
            "https://s1.ax1x.com/2018/06/22/PpyLfH.jpg",
            "https://s1.ax1x.com/2018/06/22/PpBWrT.jpg",
            "https://s1.ax1x.com/2018/06/22/PprOED.jpg",
            "https://s1.ax1x.com/2018/06/22/PpBDaQ.jpg",
            "https://s1.ax1x.com/2018/06/22/Pp6Vcn.jpg",
            "https://s1.ax1x.com/2018/06/22/PprxCd.jpg",
            "https://s1.ax1x.com/2018/06/22/Pp6QNF.jpg",
            "https://s1.ax1x.com/2018/06/22/Pp6itg.jpg",
            "https://s1.ax1x.com/2018/06/22/Pp6Vcn.jpg",
            "https://s1.ax1x.com/2018/06/22/Ppyj1A.jpg",
            "https://s1.ax1x.com/2018/06/22/PpByPs.jpg",
            "https://s1.ax1x.com/2018/06/22/PpB85d.jpg",
            "https://s1.ax1x.com/2018/06/22/PpByPs.jpg",
            "https://s1.ax1x.com/2018/06/22/PprHu6.jpg",
            "https://s1.ax1x.com/2018/06/22/PpsSgI.jpg",
            "https://s1.ax1x.com/2018/06/22/PpBJPA.jpg",
            "https://s1.ax1x.com/2018/06/22/PpsPDf.jpg",
            "https://s1.ax1x.com/2018/06/22/Pp6SnP.jpg",
            "https://s1.ax1x.com/2018/06/22/PprgBT.jpg",
            "https://s1.ax1x.com/2018/06/22/PpBwqS.jpg",
            "https://s1.ax1x.com/2018/06/22/PpsPDf.jpg",
            "https://s1.ax1x.com/2018/06/22/PpBNxP.jpg",
            "https://s1.ax1x.com/2018/06/22/Ppypi4.jpg",
            "https://s1.ax1x.com/2018/06/22/Ppyv6I.jpg",
            "https://s1.ax1x.com/2018/06/22/Pp6978.jpg",
            "https://s1.ax1x.com/2018/06/22/PpsvZT.jpg",
            "https://s1.ax1x.com/2018/06/22/PprTjx.jpg",
            "https://s1.ax1x.com/2018/06/22/PpBNxP.jpg",
            "https://s1.ax1x.com/2018/06/22/Pps5dS.jpg",
            "https://s1.ax1x.com/2018/06/22/PpBgx0.jpg"]

for i in range(100):
    sql = "INSERT INTO user (avatar, birthday, email, gender, `level`, mobile, nickname, password, token, username) " \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    gender = random.randint(0,1)
    nickname = [faker.name_male(), faker.name_female()]
    cursor.execute(sql, [avatars[random.randint(0, len(avatars)-1)], faker.date_between(start_date='-20y', end_date='-10y'),
                            faker.ascii_email(), gender, random.randint(1,5), faker.phone_number(),
                            nickname[gender], "pbkdf2_sha256$20000$gcIJmE3uEhjo$N+KnrSXZByhF961PVuDtl3vPqehUrbb0FO4jaJqAtmw=",
                         faker.uuid4(), faker.user_name()])
    db.commit()
    print(i)

