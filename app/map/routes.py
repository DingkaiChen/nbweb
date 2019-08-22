import os
from app.map.forms import SoilshpForm
from app.models import Soilindicator,Soildata,Soilplot,Soilshp
from flask import render_template, flash, redirect, url_for, request, current_app
from app import db
from werkzeug.urls import url_parse
from werkzeug import secure_filename
import xlrd
import re
from datetime import date,datetime
from app.map import bp
from flask_login import current_user,login_required

@bp.route("/soilurl",methods=["GET","POST"])
@login_required
def soilurl():
	if not current_user.check_roles(['admin']):
		flash('非系统管理员用户无权访问该页面')
		return redirect(url_for('main.index'))
	form=SoilshpForm()
	form.indicators.choices=[(item.id,item.indicatorname) for item in Soilindicator.query.all()]
	wdatas=Soildata.query.order_by(Soildata.year).all()
	form.years.choices=[]
	existyear=None
	if len(wdatas)>0:
		existyear=wdatas[0].year
		for item in wdatas:
			if item.year!=existyear:
				form.years.choices.append((existyear,existyear))
				existyear=item.year
		form.years.choices.append((existyear,existyear))
	wdatas=Soilplot.query.order_by(Soilplot.region).all()
	form.regions.choices=[]
	existregion=None
	if len(wdatas)>0:
		existregions=wdatas[0].region
		for item in wdatas:
			if item.region!=existregion:
				form.regions.choices.append((existregion,existregion))
				existregion=item.region
		form.regions.choices.append((existregion,existregion))
	if request.method=='POST' and (form.action.data is not None):
		if form.action.data==2:#action: '0' for ADD, '1' for EDIT, '2' for 'DELETE', '3' for excel file upload
			shp=Soilshp.query.filter_by(id=form.id.data).first()
			if shp is None:
				flash('链接删除失败！')
			else:
				indicatorname=shp.indicator.indicatorname
				db.session.delete(shp)
				db.session.commit()
				flash('指标 <{}> 链接删除成功！'.format(indicatorname))
		elif form.action.data==0:
			shp=Soilshp(indicator_id=form.indicators.data,\
				region=form.regions.data,\
				year=form.years.data,\
				shpurl=form.shp.data)
			db.session.add(shp)
			db.session.commit()
			flash('指标 <{}> 链接添加成功！'.format(shp.indicator.indicatorname))
		elif form.action.data==1:
			shp=Soilshp.query.filter_by(id=form.id.data).first()
			if shp:
				shp.shpurl=form.shp.data
				db.session.commit()
				flash('指标 <{}> 链接编辑成功！'.format(shp.indicator.indicatorname))
			else:
				flash('指标链接编辑失败！')
	shps=Soilshp.query.order_by(Soilshp.year,Soilshp.region,Soilshp.indicator_id).all()
	return render_template('map/soilurl.html',title='地图服务管理',shps=shps, form=form)
