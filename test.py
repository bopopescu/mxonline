# #-*-coding: utf-8 -*-
# _author_ = 'HBL'
# _date_ = '2020/3/3 14:30'
#
# # coding:utf-8
# import smtplib
# from email.mime.text import MIMEText  # 引入smtplib和MIMEText
#
# host = 'smtp.qq.com'  # 设置发件服务器地址
# port = 25  # 设置发件服务器端口号。注意，这里有SSL和非SSL两种形式
# sender = '415441075@qq.com'  # 设置发件邮箱，一定要自己注册的邮箱
# pwd = 'eokikhsbkekzbhhd'  # 设置发件邮箱的密码，等会登陆会用到
# receiver = '415441075@qq.com'  # 设置邮件接收人，可以是扣扣邮箱
# body = '<h1>Hi</h1><p>test</p>'  # 设置邮件正文，这里是支持HTML的
#
# msg = MIMEText(body, 'html')  # 设置正文为符合邮件格式的HTML内容
# msg['subject'] = 'Hello world'  # 设置邮件标题
# msg['from'] = sender  # 设置发送人
# msg['to'] = receiver  # 设置接收人
#
# try:
# 	s = smtplib.SMTP(host, port)  # 注意！如果是使用SSL端口，这里就要改为SMTP_SSL
# 	s.login(sender, pwd)  # 登陆邮箱
# 	s.sendmail(sender, receiver, msg.as_string())  # 发送邮件！
# 	print('Done')
# except smtplib.SMTPException:
# 	print('Error')
#

