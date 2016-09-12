#coding=utf-8
#!/usr/bin/python
import sys
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr

def sendemail(appName):
  def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))
 
  from_addr = '119923856@qq.com'
  password = 'wvopidfddiaicafb'
  to_addr = '717947120@qq.com'
  # to_addr = 'zhuangxiaowei_dev@163.com'
  smtp_server = 'smtp.qq.com'
  
  msg = MIMEText('新版本( <a href="http://fir.im/weishengshu" style="color:red;font-size:20px">' + appName + '</a>) 已经更新', 'html', 'utf-8')
  msg['From'] = _format_addr('来自 自动打包 <%s> ' % from_addr)
  msg['To'] = _format_addr('to <%s> ' % to_addr)
  msg['Subject'] = Header(u'测试版本更新提醒').encode()

  server = smtplib.SMTP_SSL(smtp_server, 465)
  server.set_debuglevel(1)
  server.login(from_addr, password)
  server.sendmail(from_addr, [to_addr], msg.as_string())
  server.quit()

name = sys.argv[1]
print name
if name == None:
  name = '测试版本更新'
sendemail(name) 
  
