from flask import current_app,render_template
from flask_mail import Message
from threading import Thread
from app import mail

WEBSITE_NAME='宁波城市环境观测网'

def send_async_email(app,msg):
	with app.app_context():
		mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
	msg=Message(subject, sender=sender,recipients=recipients)
	msg.body=text_body
	msg.html=html_body
	Thread(target=send_async_email,args=(current_app._get_current_object(),msg)).start()

def send_password_reset_email(user):
	token=user.get_reset_password_token()
	send_email('[{}] 密码重置'.format(WEBSITE_NAME),\
		sender=current_app.config['ADMINS'][0],\
		recipients=[user.email],\
		text_body=render_template('email/reset_password.txt',user=user,token=token),\
		html_body=render_template('email/reset_password.html',user=user,token=token))

def send_register_verify_email(register):
	token=register.get_register_verify_token()
	send_email('[{}] 注册邮箱认证'.format(WEBSITE_NAME),\
		sender=current_app.config['ADMINS'][0],\
		recipients=[register.email],\
		text_body=render_template('email/register_verify.txt',user=register,token=token),\
		html_body=render_template('email/register_verify.html',user=register,token=token))

def send_accept_email(user):
	send_email('[{}] 注册审核通过'.format(WEBSITE_NAME),\
		sender=current_app.config['ADMINS'][0],\
		recipients=[user.email],\
		text_body=render_template('email/accept_user.txt',user=user),\
		html_body=render_template('email/accept_user.html',user=user))

def send_reject_email(user):
	send_email('[{}] 注册审核信息'.format(WEBSITE_NAME),\
		sender=current_app.config['ADMINS'][0],\
		recipients=[user.email],\
		text_body=render_template('email/reject_user.txt',user=user),\
		html_body=render_template('email/reject_user.html',user=user))
