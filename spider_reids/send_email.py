# -*- coding:utf-8 -*-
import smtplib


def send_mail(body):
    smtp_server = 'smtp.163.com'
    # 用户名
    from_mail = '163邮箱'
    # 邮箱密码
    mail_pass = '通行证'
    # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    to_mail = ******
    # 抄送人
    cc_mail = [******]
    from_name = '******'
    subject = u'服务器爬虫状态监控'.encode('gbk')  # 以gbk编码发送，一般邮件客户端都能识别
    # 邮件格式:
    #     msg = '''\
    # From: %s <%s>
    # To: %s
    # Subject: %s
    # %s''' %(from_name, from_mail, to_mail_str, subject, body)  # 这种方式必须将邮件头信息靠左，也就是每行开头不能用空格，否则报SMTP 554
    mail = [
        "From: %s <%s>" % (from_name, from_mail),
        "To: %s" % ','.join(to_mail),  # 转成字符串，以逗号分隔元素
        "Subject: %s" % subject,
        "Cc: %s" % ','.join(cc_mail),
        "",
        body
    ]
    msg = '\n'.join(mail)  # 这种方式先将头信息放到列表中，然后用join拼接，并以换行符分隔元素，结果就是和上面注释一样了
    try:
        s = smtplib.SMTP()
        s.connect(smtp_server, '25')
        s.login(from_mail, mail_pass)
        s.sendmail(from_mail, to_mail + cc_mail, msg)
        s.quit()
    except smtplib.SMTPException as e:
        print "Error: %s" % e


if __name__ == "__main__":
    send_mail("爬虫结束了")
