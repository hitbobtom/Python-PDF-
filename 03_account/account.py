# python读取excel数据并导入到mysql中
# 使用hadoop100虚拟机上安装的mysql数据库，通过superset进行大屏展示
# -*- codeing = utf-8 -*-

import pymysql
import openpyxl


#################### 获取mysql连接 ####################
def getConnection():
    # host = 'localhost'
    host = 'hadoop100'
    user = 'root'
    password = '000000'
    db = 'image'
    connection = pymysql.connect(host=host, user=user, password=password, db=db)
    return connection


#################### 插入数据 ####################
def insertMysql(datalist):
    # 1.mysql
    conn = getConnection()
    # 获得游标对象
    cursor = conn.cursor()

    cursor.execute("truncate table account_info")

    # 2.处理数据
    for i in range(len(datalist)):
        data = datalist[i]

        insert = (
            "insert into account_info(`payment_time`, `description`, `trading_venues`, `amount`, `account_name`, `first_stage_ranking`,`second_stage_ranking`,`notes`,`year`,`month`,`day`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        data = (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10])
        print(data)

        cursor.execute(insert, data)
    conn.commit()
    conn.close()


#################### 读取excel ####################
def readExcel(path):
    datalist = []
    # 打开Excel文件
    workbook = openpyxl.load_workbook(path)

    # 选择工作表

    worksheet = workbook.get_sheet_by_name("支出")

    # 循环遍历行并将它们插入到数据库中
    for row in worksheet.iter_rows(min_row=2, values_only=True):
        data = []
        data.append(row[0])
        data.append(row[1])
        data.append(row[2])
        data.append(row[3])
        data.append(row[4])
        data.append(row[5])
        data.append(row[6])
        data.append(row[7])

        data.append(row[0].year)
        data.append(row[0].month)
        data.append(row[0].day)

        print('data: ' + str(data))

        datalist.append(data)

    return datalist


if __name__ == "__main__":
    path = 'C:\\Users\\sunny\\Pictures\\Saved Pictures\\账单\\account.xlsx'
    datalist = readExcel(path)
    insertMysql(datalist)
