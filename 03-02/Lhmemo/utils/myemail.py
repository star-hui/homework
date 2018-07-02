import smtplib
from email import encoders  # 附件的编码
from email.header import Header  # 邮件的主题格式
from email.mime.base import MIMEBase  # 附件
from email.mime.multipart import MIMEMultipart  # 邮件的格式，多格式
from email.mime.text import MIMEText  # 邮件的格式，纯文本格式
from email.utils import formataddr  # 邮件的发件人格式
from smtplib import SMTP_SSL
from functools import wraps

'''
构造成类
'''
class NoMailListErrot(Exception):
    '自定义异常，在邮件接收人不存在的时候，主动抛出异常'
    pass


class MailMaster:
    def __init__(self, email_from_addr='459900477@qq.com', password='iajeclsnsrxebjgd', email_server='smtp.qq.com'):
        '''初始化函数，生成smtp对象，连接到服务器，并登入进去
        '''
        # 第一步连接到服务器，并发送一个地址查询，然后登入进去
        self.smtp = SMTP_SSL(email_server)
        # self.smtp.set_debuglevel(1)  # 调试接口
        self.smtp.ehlo(email_server)
        self.email_from_addr = email_from_addr
        self.smtp.login(self.email_from_addr, password)
        self.email_to_addr = []

    def notice(self, username, text, subject='通知消息'):
        '发送通知，调用通用发邮件接口'
        self.send_email(subject, f'{username}\n'+text)

    def add_emali_to_list(self, addr: str):
        '添加收件人'
        self.email_to_addr.append(addr)
            
    def send_email(self, subject, body, mailtype='plain', attachment=None):
        '''发送邮件接口
        @subject: 邮件主题
        @body: 邮件内容
        @mailtype：邮件类型，默认时文本，发html时为html
        attachment:附件
        '''
        msg = MIMEMultipart()

        # 设置邮件的内容:标题，发件人，收件人
        msg['subject'] = Header(subject, 'utf-8')          # 邮件标题对象添加标题
        msg['from'] = formataddr(('LH', self.email_from_addr))  # 添加发件人

        try:
            if len(self.email_to_addr) > 0:
                msg['to'] = ','.join(self.email_to_addr)  # 添加收件人
            else:
                raise NoMailListErrot('还没添加收件人了，去加下吧')
        
            # body代表发送的内容，mailtype为内容的格式：文本(plian)或html
            msg.attach(MIMEText(body, mailtype, 'utf-8'))  # 定义邮件的格式

            # 如果有附件，则添加进去
            if attachment:
                # 使用二进制模式打开
                with open(attachment, 'rb') as f:
                    # MIMEBase表示附件对象
                    mime = MIMEBase('text', 'txt', filename=attachment)

                    # 第一个参数必须一致，第二个参数随意，第三个参数为附件的名字
                    mime.add_header('Content-Disposition', '456', filename='hui.py')  
                    mime.set_payload(f.read())  # 读取文件的内容到付件中
                    encoders.encode_base64(mime)  # 定义传输的编码协议，避免错落

                    msg.attach(mime)  # 将附件添加到邮件中

            self.smtp.sendmail(self.email_from_addr, self.email_to_addr, msg.as_string())  # 发送邮件
            self.smtp.quit()

        except smtplib.SMTPException as e:
            print(e)

def main():
    e = MailMaster()
    e.add_emali_to_list('2323449277@qq.com')
    e.add_emali_to_list('18768196753@139.com')
    e.notice('娄辉', '注册成功！！')

if __name__ == '__main__':
    main()
