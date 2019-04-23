import os
import json
from app.models import Societyindicator,Societyindicator,Societydata
from app.society.forms import SocietydataqueryForm
from flask import render_template, flash, redirect, url_for, request, current_app, send_file, send_from_directory
from app import db
from werkzeug.urls import url_parse
from werkzeug import secure_filename
import xlrd
import re
from datetime import date,datetime
from app.society import bp
from flask_login import current_user,login_required

ALLOWED_EXTENSIONS=set(['txt','pdf','png','jpg','jpeg','gif','xls','xlsx','csv'])

@bp.route("/data",methods=["GET","POST"])
@login_required
def data():
	if not current_user.check_roles(['admin','society']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	
	form=SocietydataqueryForm()
	societydatas=Societydata.query.order_by(Societydata.year).all()
	form.years.choices=[]
	existyear=None
	if len(societydatas)>0:
		existyear=societydatas[0].year
		for item in societydatas:
			if item.year!=existyear:
				form.years.choices.append((existyear,str(existyear)))
				existyear=item.year
		form.years.choices.append((existyear,str(existyear)))
	form.indicators.choices=[(indicator.id,'{} --> {}'.format(indicator.societyclass.classname,indicator.indicatorname)) for indicator in Societyindicator.query.order_by(Societyindicator.class_id,Societyindicator.indicatorname).all()]
	societydatas=[]
	indicators=[]
	years=[]
	if request.method=='POST' and request.form['action']:
		if form.action.data==1:
			indicators=Societyindicator.query.filter(Societyindicator.id.in_(form.indicators.data)).order_by(Societyindicator.class_id,Societyindicator.id).all()
			years=form.years.data
			for indicator in indicators:
				data=Societydata.query.filter_by(indicator_id=indicator.id).filter(Societydata.year.in_(years)).all()
				if data:
					societydata=[indicator,data]
					societydatas.append(societydata)
	return render_template('society/data.html',title='社会经济调查数据',form=form,datas=societydatas,indicators=indicators,years=years)

@bp.route('/deldata',methods=['POST'])
@login_required
def deldata():
	if not current_user.check_roles(['admin','society']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	try:
		year=request.form['year']
		indicatorid=request.form['indicatorid']
		years=request.form['years']
		indicatorids=request.form['indicators']
		years=json.loads(years)
		indicatorids=json.loads(indicatorids)
		if year=='0':
			datas=Societydata.query.filter(Societydata.indicator_id==indicatorid,Societydata.year.in_(years)).all()
			if datas is None:
				return 'fail'
			else:
				for item in datas:
					db.session.delete(item)
				db.session.commit()
		else:
			data=Societydata.query.filter(Societydata.indicator_id==indicatorid,Societydata.year==year).first()
			if data is None:
				return 'fail'
			else:
				db.session.delete(data)
				db.session.commit()
		societydatas=[]
		indicators=[]
		indicators=Societyindicator.query.filter(Societyindicator.id.in_(indicatorids)).order_by(Societyindicator.class_id,Societyindicator.id).all()
		for indicator in indicators:
			data=Societydata.query.filter_by(indicator_id=indicator.id).filter(Societydata.year.in_(years)).all()
			if data:
				societydata=[indicator,data]
				societydatas.append(societydata)
		intyears=[]
		existyear=None
		yeardatas=Societydata.query.filter(Societydata.year.in_(years)).order_by(Societydata.year).all()
		if len(yeardatas)>0:
			existyear=yeardatas[0].year
			for item in yeardatas:
				if item.year!=existyear:
					intyears.append(existyear)
				existyear=item.year
			intyears.append(existyear)
		return render_template('society/_datas.html',datas=societydatas,years=intyears)
	except:
		return 'fail'

@bp.route('/editdata',methods=['POST'])
@login_required
def editdata():
	if not current_user.check_roles(['admin','society']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
#	try:
	if True:
		year=request.form['year']
		indicatorid=request.form['indicatorid']
		value=float(request.form['value'])
		years=request.form['years']
		indicatorids=request.form['indicators']
		years=json.loads(years)
		indicatorids=json.loads(indicatorids)
		data=Societydata.query.filter(Societydata.indicator_id==indicatorid,Societydata.year==year).first()
		if data is None:
			data=Societydata(indicator_id=indicatorid,year=year,value=value)
			db.session.add(data)
		else:
			data.value=value
		db.session.commit()
		societydatas=[]
		indicators=[]
		indicators=Societyindicator.query.filter(Societyindicator.id.in_(indicatorids)).order_by(Societyindicator.class_id,Societyindicator.id).all()
		for indicator in indicators:
			data=Societydata.query.filter_by(indicator_id=indicator.id).filter(Societydata.year.in_(years)).all()
			if data:
				societydata=[indicator,data]
				societydatas.append(societydata)
		intyears=[]
		existyear=None
		yeardatas=Societydata.query.filter(Societydata.year.in_(years)).order_by(Societydata.year).all()
		if len(yeardatas)>0:
			existyear=yeardatas[0].year
			for item in yeardatas:
				if item.year!=existyear:
					intyears.append(existyear)
				existyear=item.year
			intyears.append(existyear)
		return render_template('society/_datas.html',datas=societydatas,years=intyears)
#	except:
#		return 'fail'



