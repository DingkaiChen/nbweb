from app import db
from app.auth import bp
from app.auth.forms import LoginForm,RegistrationForm,ResetPasswordRequestForm,ResetPasswordForm
from app.models import User,Role,Register
from app.email import send_password_reset_email,send_register_verify_email,send_reject_email,send_accept_email
from flask import render_template,flash,redirect,url_for,request
from flask_login import current_user,login_user,logout_user,login_required
from werkzeug.urls import url_parse

@bp.route('/login',methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form=LoginForm()
	if form.validate_on_submit():
		user=User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('用户名或密码无效')
			return redirect(url_for('auth.login'))
		login_user(user,remember=form.remember_me.data)
		next_page=request.args.get('next')
		if not next_page or url_parse(next_page).netloc!='':
			next_page=url_for('main.index')
		return redirect(next_page)
	return render_template('auth/login.html',title='登录',form=form)

@bp.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.index'))

@bp.route('/register',methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form=RegistrationForm()
	if form.validate_on_submit():
		register=Register(username=form.username.data,email=form.email.data,name=form.name.data,phone=form.phone.data,verified=0)
		register.set_password(form.password.data)
		
		db.session.add(register)
		db.session.commit()
		send_register_verify_email(register)
		flash('您的申请已提交，系统将自动发送确认邮件至您填写的邮箱地址，请通过该邮件进行邮箱地址认证!')
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html',title='注册',form=form)

@bp.route('/reset_password_request',methods=['GET','POST'])
def reset_password_request():
	if current_user.is_authenticated:
		return redirect(url_for('auth.index'))
	form=ResetPasswordRequestForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		if user:
			send_password_reset_email(user)
		flash('请查收邮件并根据邮件内容重置密码.')
		return redirect(url_for('auth.login'))
	return render_template('auth/reset_password_request.html',title='密码重置申请',form=form)

@bp.route('/reset_password/<token>',methods=['GET','POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	user=User.verify_reset_password_token(token)
	if not user:
		return redirect(url_for('main.index'))
	form=ResetPasswordForm()
	if form.validate_on_submit():
		user.set_password(form.password.data)
		db.session.commit()
		flash('密码已重置.')
		return redirect(url_for('auth.login'))
	return render_template('auth/reset_password.html',title='密码重置',form=form)

@bp.route('/register_verify/<token>',methods=['GET'])
def register_verify(token):
	if current_user.is_authenticated:
		print('0')
		return redirect(url_for('main.index'))
	register=Register.verify_register_verify_token(token)
	if not register:
		print('1')
		return redirect(url_for('main.index'))
	register.verify()
	db.session.commit()
	flash('邮箱认证成功！请等待系统管理员审核，审核时间大约1-2个工作日。')
	return redirect(url_for('main.index'))

@bp.route('/newusers',methods=['GET'])
@login_required
def newusers():
	if not current_user.check_roles(['admin']):
		flash('非系统管理员用户无权访问该页面')
		return redirect(url_for('main.index'))
	newusers=Register.query.filter_by(verified=1).all()
	print(newusers)
	return render_template('auth/newusers.html',title='用户审核',newusers=newusers)
	
@bp.route('/acceptnewuser',methods=['POST'])
@login_required
def acceptnewuser():
	if not current_user.check_roles(['admin']):
		flash('非系统管理员用户无权访问该页面')
		return redirect(url_for('main.index'))
	register_id=request.form['id']
	register=Register.query.filter_by(id=register_id).first()
	if register is None:
		return 'fail'
	else:
		user=User(username=register.username,\
			email=register.email,\
			password_hash=register.password_hash,\
			name=register.name,\
			phone=register.phone)
		role=Role.query.filter_by(rolename='general').first()
		user.roles.append(role)
		db.session.add(user)
		db.session.delete(register)
		db.session.commit()
		send_accept_email(user)
		newusers=Register.query.filter_by(verified=1).all()
		return render_template('auth/_newusers.html',newusers=newusers)
		
@bp.route('/rejectnewuser',methods=['POST'])
@login_required
def rejectnewuser():
	if not current_user.check_roles(['admin']):
		flash('非系统管理员用户无权访问该页面')
		return redirect(url_for('main.index'))
	register_id=request.form['id']
	register=Register.query.filter_by(id=register_id).first()
	if register is None:
		return 'fail'
	else:
		db.session.delete(register)
		db.session.commit()
		send_reject_email(register)
		newusers=Register.query.filter_by(verified=1).all()
		return render_template('auth/_newusers.html',newusers=newusers)
		
		
