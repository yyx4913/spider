from lxml import etree

def getCookies(username, password):
    headers = {
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
        "Referer": "https://passport.weibo.cn/signin/login?entry=mweibo&r=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt="
    }
    cks = {}
    post_data = {
        'username': username,
        'password': password,
        'savestate':  1,
        'r': 'http://weibo.cn/',
        'ec':  1,
        'entry': 'mweibo',
        'mainpageflag': 1,

    }
    login_url = 'https://passport.weibo.cn/sso/login'
    f = requests.post(url=login_url,headers=headers, data=post_data)  # 打开Charles的同时运行程序报错，可在此加上verify=False
    cks.update(dict(f.cookies))
    return cks

if __name__ == '__main__':
    username = '********' # 用户名
    password = '***********'  # 密码
    cks = getCookies(username, password)
    test_url = 'https://weibo.cn/2714280233/fans'  # 测试页面
    text = requests.get(url=test_url, cookies=cks).content  # 在此使用content，使用text可能出错,python2
    res = etree.HTML(text)
    print res.xpath('//div[@class="c"]/table[3]//a[1]/text()')

