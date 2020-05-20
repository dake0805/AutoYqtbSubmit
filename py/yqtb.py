import time

import pymysql
import requests
from lxml import etree


def login(account, password):
    user = requests.session()
    getResult = user.get('https://uis.nwpu.edu.cn/cas/login')
    JSESSIONID = dict(getResult.cookies)['JSESSIONID']
    print(JSESSIONID)
    form_data_lt = str(etree.HTML(getResult.content).xpath('//input[@name="lt"]/@value')[0])
    header = {
        'Origin': 'https://uis.nwpu.edu.cn',
        'Referer': 'https://uis.nwpu.edu.cn/cas/login',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
    postData = {
        'username': account,
        'password': password,
        'imageCodeName': '',
        'lt': form_data_lt,
        '_eventId': 'submit'
    }
    postResponse = user.post('https://uis.nwpu.edu.cn/cas/login;jsessionid=' + JSESSIONID, data=postData,
                             headers=header)
    cookie = postResponse.cookies
    return user


def yqtb(cookie, account, location, zip, hubei, name, xueyuan, cellphone):
    if (hubei == 1):
        data = {
            'sfczbcqca': '',
            'czbcqcasjd': '',
            'sfczbcfhyy': '',
            'czbcfhyysjd': '',
            'actionType': 'addRbxx',
            'userLoginId': account,
            'fxzt': 2,
            'userType': 2,
            'userName': name,
            'szcsbm': zip,  # 所在城市 2：在西安 3：其他
            'szcsmc': location,  # 所在城市名称
            'sfjt': '1',  # 是否经停
            'sfjtsm': '人在湖北',  # 是否经停说明
            'sfjcry': '1',  # 是否接触人员
            'sfjcrysm': '人在湖北',  # 是否接触人员说明
            'sfjcqz': '0',  # 是否接触确诊
            'sfyzz': '0',  # var sfyzz =  $('input[name='radio5']:checked').val();
            'sfqz': '0',  # 是否确诊
            'ycqksm': '',  # 异常情况说明
            'glqk': '0',  # 隔离情况
            'glksrq': '',  # 隔离开始日期
            'gljsrq': '',  # 隔离结束日期
            'tbly': 'sso',  # what's this?
            'glyy': '',  # 隔离原因
            'qtqksm': '',
            'sfjcqzsm': '',  # 是否接触确诊说明
            'sfjkqk': '0',
            'jkqksm': '',
            'sfmtbg': '',
            'qrlxzt': '',
            'xymc': xueyuan,
            'xssjhm': cellphone
        }
    else:
        data = {
            'sfczbcqca': '',
            'czbcqcasjd': '',
            'sfczbcfhyy': '',
            'czbcfhyysjd': '',
            'actionType': 'addRbxx',
            'userLoginId': account,
            'fxzt': 2,
            'userType': 2,
            'userName': name,
            'szcsbm': zip,  # 所在城市 2：在西安 3：其他
            'szcsmc': location,  # 所在城市名称
            'sfjt': '0',  # 是否经停
            'sfjtsm': '',  # 是否经停说明
            'sfjcry': '0',  # 是否接触人员
            'sfjcrysm': '',  # 是否接触人员说明
            'sfjcqz': '0',  # 是否接触确诊
            'sfyzz': '0',  # var sfyzz =  $('input[name='radio5']:checked').val();
            'sfqz': '0',  # 是否确诊
            'ycqksm': '',  # 异常情况说明
            'glqk': '0',  # 隔离情况
            'glksrq': '',  # 隔离开始日期
            'gljsrq': '',  # 隔离结束日期
            'tbly': 'sso',  # what's this?
            'glyy': '',  # 隔离原因
            'qtqksm': '',
            'sfjcqzsm': '',  # 是否接触确诊说明
            'sfjkqk': '0',
            'jkqksm': '',
            'sfmtbg': '',
            'qrlxzt': '',
            'xymc': xueyuan,
            'xssjhm': cellphone
        }

    header = {
        'Origin': 'http://yqtb.nwpu.edu.cn',
        'Referer': 'http://yqtb.nwpu.edu.cn/wx/ry/jrsb.jsp',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
    }
    user = requests.session()
    result = user.post('http://yqtb.nwpu.edu.cn/wx/ry/ry_util.jsp',
                       cookies=cookie,
                       data=data,
                       headers=header)
    print(result.text)
    if ("{\"state\":1}" not in result.text):
        print("error")
        exit(0)


def run():
    db = pymysql.connect(host="localhost", port=3306, user="dake0805", passwd="",
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
        hubei = row[5]
        name = row[6]
        user = login(account, password)
        cookie = user.cookies
        if "CASTGC" in dict(cookie).keys():
            user.get("http://yqtb.nwpu.edu.cn/wx/xg/yz-mobile/index.jsp")
            getResult = user.get("http://yqtb.nwpu.edu.cn/wx/ry/jbxx_v.jsp")
            cellphone = (etree.HTML(getResult.content).xpath('//label[text()="手机号码："]/../../span/text()')[0])
            xueyuan = str(etree.HTML(getResult.content).xpath('//label[text()="学院/大类："]/../../span/text()')[0])

            yqtb(cookie, account, location, zip, hubei, name, xueyuan, cellphone)

            time.sleep(30)
        else:
            print("login error")


if __name__ == '__main__':
    run()
