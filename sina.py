# coding:utf-8
import urllib,base64,re,json,requests,sys,urllib2
import rsa,binascii,cookielib


reload(sys)
sys.setdefaultencoding("utf8")



def get_encrypted_pw(password, data): # 密码加密

    rsa_e = int('10001',16) # 十六进制转十进制
    pw_string = str(data['servertime']) + '\t' + str(data['nonce']) + '\n' + str(password)
    key = rsa.PublicKey(int(data['pubkey'], 16), rsa_e)
    pw_encypted = rsa.encrypt(pw_string, key)
    password = ''
    passwd = binascii.b2a_hex(pw_encypted)  # 二进制转化为ascii
    return passwd

def Post_params(username, raw,pwd):
    post_data = {
    "entry":"weibo",
    "gateway":"1",
    "from": "",
    "savestate": "7",
    "qrcode_flag":'false',
    "useticket": "1",
    "pagerefer": "https://login.sina.com.cn/crossdomain2.php?action=logout&r=https%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl%3D%252F",
    "vsnf": "1",
    "su": username,
    "service":"miniblog",
    "servertime": raw['servertime'],
    "nonce": raw['nonce'],
    "pwencode": "rsa2",
    "rsakv": raw['rsakv'],
    "sp": pwd,
    "sr": "1680*1050",
    "encoding": "UTF-8",
    "prelt": "194",
    "url": "https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
    "returntype": "META"
    }
    return post_data

def login(password, data, user):
    url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
    headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    cks = {}
    pwd = get_encrypted_pw(password, data)
    post_data = Post_params(user, data, pwd)
    cookie = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    opener.open(url)
    cont = requests.post(url=url, headers=headers,data=post_data, cookies=cookie).text
    p1 = re.compile('location\.replace\("(.*?)"\)')
    p2 = re.compile("location\.replace\('(.*?)'\)")
    p3 = re.compile('uniqueid"\:"(.*?)"')
    url1 = p1.search(cont).group(1)
    opener.open(url1)
    cont1 = requests.post(url=url1, data=post_data, headers=headers,cookies=cookie).text
    url2 = p2.search(cont1).group(1)
    opener.open(url2)
    for ck in cookie:
        cks[ck.name] = ck.value
    cont2= requests.get(url=url2,headers=headers, cookies=cks).text
    uid = p3.search(cont2).group(1)  # 登陆首页
    final_url = 'https://weibo.com/u/'+ str(uid)
    res = requests.get(url=final_url, cookies=cks, headers=headers).text
    print res  # 验证是否登陆成功
def getData(username):
    b64user = base64.b64encode(urllib.quote(username))
    pattern = re.compile('\((.*)\)')
    url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=' + b64user + '&rsakt=mod&client=ssologin.js(v1.4.19)'
    res = requests.get(url).text
    params = pattern.search(res).group(1)
    data = json.loads(params)  # 将获得的信息json化
    return data,b64user

if __name__ =='__main__':
    username = '*******'  # 微博账号
    pwd = '***********'  # 密码
    data, b64user= getData(username)
    login(pwd,data, b64user)

