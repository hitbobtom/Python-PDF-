import pymysql


# 获取mysql连接
def getConnection():
    host = 'localhost'
    user = 'root'
    password = '123456'
    db = 'ehentai'
    connection = pymysql.connect(host=host, user=user, password=password, db=db)
    return connection


def insertMysql(datalist):
    # 1.mysql
    conn = getConnection()
    # 获得游标对象
    cursor = conn.cursor()

    # 2.处理数据
    for i in range(len(datalist)):
        data = datalist[i]

        insert = ("insert into file_info(no, flie_name, file_detail_url, thumbnail_url, category, page_size) values(%s,%s,%s,%s,%s,%s)")
        data = (data[0], data[1], data[2], data[3], data[4], data[5])
        print(data)

        cursor.execute(insert, data)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    datalist = []
    data = [1,
            '[SSB (Maririn)] Hatsutaiken, Cosplay Sex de Doutei Ubawarete Seiheki Bug chatta Hanashi [Chinese] [不咕鸟汉化组] [Digital]',
            'https://e-hentai.org/g/2646687/27f951aa11',
            'https://ehgt.org/84/6d/846dbd8af716ae0a4099519b6fa131b2ca342d38-1963433-2150-3035-jpg_250.jpg',
            'Doujinshi', 13]
    datalist.append(data)
    insertMysql(datalist)

