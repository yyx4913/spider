# 模拟新浪微博登陆

工具：Charles，Pycharm
语言： python 2.7

微博登陆，开启Charles工具，发现每次登陆是经过多次跳转重定向才到真正的登陆页面，秉承拿到cookie就是王道的宗旨，一步一步解析经过了哪些跳转：


从Charles的抓包数据得出：

	第一步：以get方式获取起始URL：http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=' + username + '&rsakt=mod&client=ssologin.js(v1.4.19)'， 值得说明是username是经过base64加密过后的用户名，返回的内容是一个字典形式的数据；

	第二步：以post方式请求名为“https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)”的文件，获取网页具体内容；
	post_data = {
		"entry":"weibo",
	    "gateway":"1",
	    "from": "",
	    "savestate": "7",
	    "qrcode_flag":'false',
	    "useticket": "1",
	    "pagerefer": "https://login.sina.com.cn/crossdomain2.php?action=logout&r=https%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl%3D%252F",
	    "vsnf": "1",
	    "su": username,  # 微博登陆账号
	    "service":"miniblog",
	    "servertime": raw['servertime'], #此处的raw是访问起始URL获得的data字典，具体看代码实现
	    "nonce": raw['nonce'], 
	    "pwencode": "rsa2",
	    "rsakv": raw['rsakv'],
	    "sp": pwd,   # 密码，此处密码不是直接的密码，需要进一步处理，具体看代码实现
	    "sr": "1680*1050",
	    "encoding": "UTF-8",
	    "prelt": "194",
	    "url": "https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
	    "returntype": "META"
	}

	第三步：使用re 从内容中匹配location.replace获取跳转URL, 获取网页内容；
	第四步：继续使用re从内容中匹配location.replace获取跳转URL， 获取网页内容；
	第五步：在此，打印出获取的内容，一些关于登陆账号的信息全部都已经出来了；

	PS：每次访问的时候记得带入cookie，或者可能失败；

	详情请看代码实现 。。。。。




偶然间看到一篇博客使用 https://weibo.cn 访问微博，并且比前面的模拟登陆pc版的简单了不是一点两点，获取的登陆内容也不是变态的js，再也不用每次拿re去匹配了， 而是可以直接用xpath解析的dome结构， 简直就是福音有没有，于是又重新写了一个m_sina.py模拟登陆

在这个spider再也没有了烦人的各种跳转解析，就是简单直接上，具体看代码实现







