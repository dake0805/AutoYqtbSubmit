import re
import time

import pymysql

from login import *
from yqtb import yqtb_inSchool
from yqtb import yqtb_out


def run():
    db = pymysql.connect(host=mysql_host, port=3306, user=mysql_username, passwd=mysql_passwd,
                         db="yqtb", charset="utf8")
    sql = """SELECT * FROM user"""
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        account = row[1]
        location = row[2]
        password = row[3]
        zip = row[4]
        # hubei = row[5]
        # name = row[6]
        inschool = row[6]

        user = login(account, password)

        if user is None:
            continue

        # 基本信息
        jbxx_html = user.get("http://yqtb.nwpu.edu.cn/wx/ry/jbxx_v.jsp")
        cellphone = (etree.HTML(jbxx_html.content).xpath('//label[text()="手机号码："]/../../span/text()')[0])
        xueyuan = str(etree.HTML(jbxx_html.content).xpath('//label[text()="学院/大类："]/../../span/text()')[0])
        name = str(etree.HTML(jbxx_html.content).xpath('//label[text()="姓名："]/../../span/text()')[0])

        jrsb_html = user.get(
            'http://yqtb.nwpu.edu.cn/wx/ry/jrsb.jsp')

        # 返校状态现在是 bdzt (报道状态？)
        fxzt1 = re.findall(r"bdzt:'\d{1,}'", re.findall(r"var paramData.*bdzt:'\d{0,}'",
                                                        jrsb_html.text,
                                                        flags=0)[0])[0]
        fxzt = re.findall(r"\d{1,}", fxzt1)[0]

        save_mode = (etree.HTML(jrsb_html.content).xpath('//a[text()="提交填报信息"]/@href')[0])

        # 已返校情况
        if "go_subfx();" in save_mode:
            yqtb_inSchool(user, account, location, zip, name, xueyuan, cellphone, inschool, fxzt)

        elif "go_sub()" in save_mode:
            yqtb_out(user, account, location, zip, name, xueyuan, cellphone, inschool, fxzt)

        time.sleep(30)
    else:
        print("login error @ main.py 45")


if __name__ == '__main__':
    run()
