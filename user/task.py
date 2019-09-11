from celery import task
from django.core.mail import send_mail
from shopping import settings


@task
def sendEmail(email, token):
    """同步"""
    title = '欢迎注册美多商城'
    content = '<a href="http://127.0.0.1:8000/user/active/?token=' + token.decode() + '">点击激活账号</a>'
    send_mail(title, content, settings.EMAIL_FORM, [email], html_message=content)
