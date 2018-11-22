#coding:utf-8
import threading
from django.core.mail import send_mail
from django.conf import settings

# 继承Thread，需要实现run方法
class SendTextEmail(threading.Thread):
    """send html email"""
    def __init__(self, subject, body, send_from, to_list, fail_silently=False):
        self.subject = subject
        self.body = body
        self.send_from = send_from
        self.to_list = to_list
        self.fail_silently = fail_silently  # 默认发送异常不报错
        threading.Thread.__init__(self)

    def run(self):
        """发送简单的文本邮件"""
        send_mail(self.subject, self.body, self.send_from, self.to_list)


def send_text_email(subject, body, to_list):
    """发送简单的文本邮件"""
    send_from = settings.DEFAULT_FROM_EMAIL
    send_email = SendTextEmail(subject, body, send_from, to_list)
    send_email.start()
    # send_mail(subject, body, send_from, to_list)

