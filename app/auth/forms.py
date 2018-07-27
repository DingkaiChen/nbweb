from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import InputRequired,DataRequired,ValidationError,Email,EqualTo
from app.models import User,Register

class LoginForm(FlaskForm):
	username=StringField('用户名',validators=[DataRequired()])
	password=PasswordField('密码',validators=[DataRequired()])
	remember_me=BooleanField('自动登录')
	submit=SubmitField('登录')

class RegistrationForm(FlaskForm):
	username=StringField('用户名',validators=[DataRequired()])
	email=StringField('电子邮箱',validators=[DataRequired(),Email()])
	password=PasswordField('密码',validators=[DataRequired()])
	password2=PasswordField('确认密码',validators=[DataRequired(),EqualTo('password')])
	phone=StringField('联系电话',validators=[InputRequired()])
	name=StringField('姓名',validators=[InputRequired()])
	submit=SubmitField('注册')

	def validate_username(self,username):
		user=User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('您所申请的用户名已被其他用户申请，请更换用户名.')
		else:
			register=Register.query.filter_by(username=username.data,verified=1).first()
			if register is not None:
				raise ValidationError('您所申请的用户名已被其他用户申请，请更换用户名.')

	def validate_email(self,email):
		user=User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('邮箱已被注册，请使用其它邮箱注册.')
		else:
			register=Register.query.filter_by(email=email.data,verified=1).first()
			if register is not None:
				raise ValidationError('邮箱已被注册，请使用其它邮箱注册.')

class ResetPasswordRequestForm(FlaskForm):
	email=StringField('电子邮箱',validators=[DataRequired(),Email()])
	submit=SubmitField('申请密码重置')

class ResetPasswordForm(FlaskForm):
	password=PasswordField('新密码',validators=[DataRequired()])
	password2=PasswordField('确认新密码',validators=[DataRequired(),EqualTo('password')])
	submit=SubmitField('更改密码')

class UsersForm(FlaskForm):
	id=IntegerField('ID')
	action=IntegerField('action')
	role=SelectField('角色',coerce=int,validators=[DataRequired()])
	submit=SubmitField('确定')
