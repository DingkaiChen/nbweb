import os
import json
from app.soil.forms import SoilplotForm,SoildataqueryForm,SoilindicatorForm
from app.models import Soilplot,Soilindicator,Soildata
from flask import render_template, flash, redirect, url_for, request, current_app, send_file, send_from_directory
from app import db
from werkzeug.urls import url_parse
from werkzeug import secure_filename
import xlrd
import re
from datetime import date,datetime
from app.soil import bp
from flask_login import current_user,login_required

ALLOWED_EXTENSIONS=set(['txt','pdf','png','jpg','jpeg','gif','xls','xlsx','csv'])

@bp.route("/plot",methods=["GET","POST"])
@login_required
def plot():
	if not current_user.check_roles(['admin','soil']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	form=SoilplotForm()
	form.region.choices=[('北仑城区网格化采样','北仑城区网格化采样'),('城郊乡梯度流域采样','城郊乡梯度流域采样')]
	if request.method=='POST' and (form.action.data is not None):
		if form.action.data==3:#action: '0' for ADD, '1' for EDIT, '2' for 'DELETE', '3' for excel file upload
			file=request.files['file']
			if file and allowed_file(file.filename):
				filename=secure_filename(file.filename)
				filepath=os.path.join(current_app.config['UPLOAD_FOLDER'],filename)
				file.save(filepath)
				workbook=xlrd.open_workbook(filepath)
				hassheet=False
				for sheetname in workbook.sheet_names():
					if sheetname.find('土壤调查样点')>=0:
						result=insert_soilplots(sheet=workbook.sheet_by_name(sheetname),workbook=workbook)
						if result>0:
							flash('数据上传完成，已成功添加数据 {} 条'.format(str(result)))
						elif result==0:
							flash('数据上传完成，未添加任何数据')
						else:
							flash('数据上传失败')
						hassheet=True
				if hassheet==False:
					flash('上传文件中未找到表 “土壤调查样点”。请上传规范格式的文件，具体请参考模板。')
			else:
				flash('出错：请上传规范格式的文件，具体请参考模板。')	
		elif form.action.data==2:
			plot=Soilplot.query.filter_by(id=form.id.data).first()
			if plot is None:
				flash('样地删除失败！')
			else:
				for data in plot.soildatas:
					db.session.delete(data)
				db.session.delete(plot)
				db.session.commit()
				flash('土壤样地 <{}> 删除成功！'.format(plot.plotname))
		elif form.action.data==0:
			plot=Soilplot(plotname=form.plotname.data,\
				region=form.region.data,\
				frequency=form.frequency.data,\
				latdegree=form.latdegree.data,\
				latminute=form.latminute.data,\
				latsecond=form.latsecond.data,\
				londegree=form.londegree.data,\
				lonminute=form.lonminute.data,\
				lonsecond=form.lonsecond.data,\
				altitude=form.altitude.data)
			db.session.add(plot)
			db.session.commit()
			flash('土壤样地 <{}> 添加成功！'.format(form.plotname.data))
		elif form.action.data==1:
			plot=Soilplot.query.filter_by(id=form.id.data).first()
			if plot:
				plot.region=form.region.data
				plot.frequency=form.frequency.data
				plot.latdegree=form.latdegree.data
				plot.latminute=form.latminute.data
				plot.latsecond=form.latsecond.data
				plot.londegree=form.londegree.data
				plot.lonminute=form.lonminute.data
				plot.lonsecond=form.lonsecond.data
				plot.altitude=form.altitude.data
				db.session.commit()
				flash('土壤样地 <{}> 编辑成功！'.format(form.plotname.data))
			else:
				flash('样地数据编辑失败！')
	plots=Soilplot.query.order_by(Soilplot.plotname).all()
	return render_template('soil/plot.html',title='土壤调查样地信息',plots=plots, form=form)

@bp.route('/clearplots')
@login_required
def clearplots():
	if not current_user.check_roles(['admin','soil']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	cleardata(Soildata)
	cleardata(Soilplot)
	flash('已清空土壤调查样地数据')
	return redirect(url_for('soil.plot'))

@bp.route('/download_plotexample', methods=['GET'])
@login_required
def download_plotexample():
	if not current_user.check_roles(['admin','soil']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	filename='soilplots_example.xlsx'
	filepath=os.path.join(current_app.config['DOWNLOAD_FOLDER'])
	return send_from_directory(directory=filepath, filename=filename)

@bp.route('/download_dataexample', methods=['GET'])
@login_required
def download_dataexample():
	if not current_user.check_roles(['admin','soil']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	filename='soildata_example.xlsx'
	filepath=os.path.join(current_app.config['DOWNLOAD_FOLDER'])
	return send_from_directory(directory=filepath, filename=filename)

def cleardata(dbmodel):
	datas=dbmodel.query.all()
	for data in datas:
		db.session.delete(data)
	db.session.commit()

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

def insert_soilplots(sheet,workbook):
	nrows=sheet.nrows
	count=0
	#try:
	while True:
		for i in range(1,nrows):
			row_values=sheet.row_values(i)
			plot=Soilplot.query.filter_by(plotname=row_values[0].strip(' ')).first()
			if plot is None:
				plot=Soilplot()
				plot.plotname=row_values[0].strip(' ')
				if sheet.cell(i,4).ctype==2:
					plot.frequency=int(row_values[4])
				plot.region=row_values[3].strip(' ')
				m1=re.match("(\\d+)°(\\d+)'(\\d+\\.?\\d*)\"",row_values[1].strip(' '))
				if m1:
					plot.londegree=int(m1.group(1))
					plot.lonminute=int(m1.group(2))
					plot.lonsecond=float(m1.group(3))
				m2=re.match("(\\d+)°(\\d+)'(\\d+\\.?\\d*)\"",row_values[2].strip(' '))
				if m2:
					plot.latdegree=int(m2.group(1))
					plot.latminute=int(m2.group(2))
					plot.latsecond=float(m2.group(3))
				db.session.add(plot)
				count=count+1
		db.session.commit()
		return count
	#except:
	#	return -1

@bp.route('/data',methods=['GET','POST'])
@login_required
def data():
	if not current_user.check_roles(['admin','soil']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	form=SoildataqueryForm()
	form.plots.choices=[(plot.id,plot.plotname) for plot in Soilplot.query.all()]
	#form.years.choices=[(item.year,str(item.year)) for item in Soildata.query.group_by(Soildata.year).all()]
	soildatas=Soildata.query.order_by(Soildata.year).all()
	form.years.choices=[]
	existyear=None
	if len(soildatas)>0:
		existyear=soildatas[0].year
		for item in soildatas:
			if item.year!=existyear:
				form.years.choices.append((existyear,str(existyear)))
				existyear=item.year
		form.years.choices.append((existyear,str(existyear)))
	form.indicators.choices=[(indicator.id,indicator.indicatorname) for indicator in Soilindicator.query.all()]
	soildatas=[]
	indicators=[]
	plots=[]
	years=[]
	if request.method=='POST' and request.form['action']:
		if request.form['action']=='0':#action: '0' for EXCEL FILE UPLOAD, '1' for QUERY
			file=request.files['file']
			if file and allowed_file(file.filename):
				filename=secure_filename(file.filename)
				filepath=os.path.join(current_app.config['UPLOAD_FOLDER'],filename)
				file.save(filepath)
				workbook=xlrd.open_workbook(filepath)
				hassheet=False
				for sheetname in workbook.sheet_names():
					try:
						year=int(sheetname)
					except:
						year=-1
					if year>=0:
						added_indicators=check_indicators(sheet=workbook.sheet_by_name(sheetname),workbook=workbook)
						if len(added_indicators)>0:
							flash('已添加指标项 {} 共{}项'.format('，'.join(added_indicators),len(added_indicators)))
						result=insert_soildatas(sheet=workbook.sheet_by_name(sheetname),workbook=workbook,year=year)
						if result[0]>0:
							str1='数据上传完成，共上传数据 {} 条。'.format(str(result[1]+result[2]))
							str2=''
							if result[2]>0:
								str2='{} 条数据已存在，跳过未添加。'.format(str(result[2]))
							if result[1]>0:
								db.session.commit()
								str3='已成功添加数据 {} 条。'.format(str(result[1]))
							elif result[1]==0:
								str3='未添加任何数据。'
							flash(str1+str2+str3)
						else:
							flash('数据上传失败！'+result[1])
						hassheet=True
						#form.years.choices=[(item.year,str(item.year)) for item in Soildata.query.group_by(Soildata.year).all()]
						sdatas=Soildata.query.order_by(Soildata.year).all()
						form.years.choices=[]
						existyear=None
						if len(sdatas)>0:
							existyear=sdatas[0].year
							for item in sdatas:
								if item.year!=existyear:
									form.years.choices.append((existyear,str(existyear)))
									existyear=item.year
							form.years.choices.append((existyear,str(existyear)))
						form.indicators.choices=[(indicator.id,indicator.indicatorname) for indicator in Soilindicator.query.all()]
				if hassheet==False:
					flash('上传文件中未找到以年份命名的数据表。请上传规范格式的文件，具体请参考模板。')
			else:
				flash('出错：请上传规范格式的文件，具体请参考模板。')
		elif form.action.data==1:
			plots=Soilplot.query.filter(Soilplot.id.in_(form.plots.data)).all()
			indicators=Soilindicator.query.filter(Soilindicator.id.in_(form.indicators.data)).order_by(Soilindicator.id).all()
			years=form.years.data
			for plot in plots:
				for year in years:
					data=Soildata.query.filter_by(plot=plot).filter_by(year=year).filter(Soildata.indicator_id.in_(form.indicators.data)).all()
					if data:
						soildata=[plot,year,data]
						soildatas.append(soildata)
	return render_template('soil/data.html',title='土壤调查数据',form=form,datas=soildatas,indicators=indicators,plots=plots,years=years)

@bp.route('/deldata',methods=['POST'])
@login_required
def deldata():
	if not current_user.check_roles(['admin','soil']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	try:
		plotid=request.form['plotid']
		year=request.form['year']
		indicatorid=request.form['indicatorid']
		plotids=request.form['plots']
		years=request.form['years']
		indicatorids=request.form['indicators']
		plotids=json.loads(plotids)
		years=json.loads(years)
		indicatorids=json.loads(indicatorids)
		if indicatorid=='0':
			datas=Soildata.query.filter(Soildata.soilplot_id==plotid,Soildata.year==year,Soildata.indicator_id.in_(indicatorids)).all()
			if datas is None:
				return 'fail'
			else:
				for item in datas:
					db.session.delete(item)
				db.session.commit()
		else:
			data=Soildata.query.filter(Soildata.soilplot_id==plotid,Soildata.indicator_id==indicatorid,Soildata.year==year).first()
			if data is None:
				return 'fail'
			else:
				db.session.delete(data)
				db.session.commit()
		soildatas=[]
		plots=Soilplot.query.filter(Soilplot.id.in_(plotids)).all()
		indicators=Soilindicator.query.filter(Soilindicator.id.in_(indicatorids)).order_by(Soilindicator.id).all()
		for plot in plots:
			for year in years:
				data=Soildata.query.filter_by(plot=plot).filter_by(year=year).filter(Soildata.indicator_id.in_(indicatorids)).all()
				if data:
					soildata=[plot,year,data]
					soildatas.append(soildata)
		return render_template('soil/_datas.html',datas=soildatas,indicators=indicators)
	except:
		return 'fail'

@bp.route('/editdata',methods=['POST'])
@login_required
def editdata():
	if not current_user.check_roles(['admin','soil']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
#	try:
	if True:
		plotid=request.form['plotid']
		year=request.form['year']
		indicatorid=request.form['indicatorid']
		value=float(request.form['value'])
		#a=value/1
		#a=value+1
		#if value>1:
		#	a=a+1
		plotids=request.form['plots']
		years=request.form['years']
		indicatorids=request.form['indicators']
		plotids=json.loads(plotids)
		years=json.loads(years)
		indicatorids=json.loads(indicatorids)
		data=Soildata.query.filter(Soildata.soilplot_id==plotid,Soildata.indicator_id==indicatorid,Soildata.year==year).first()
		if data is None:
			data=Soildata(soilplot_id=plotid,indicator_id=indicatorid,year=year,value=value)
			db.session.add(data)
		else:
			data.value=value
		db.session.commit()
		soildatas=[]
		plots=Soilplot.query.filter(Soilplot.id.in_(plotids)).all()
		indicators=Soilindicator.query.filter(Soilindicator.id.in_(indicatorids)).order_by(Soilindicator.id).all()
		for plot in plots:
			for year in years:
				data=Soildata.query.filter_by(plot=plot).filter_by(year=year).filter(Soildata.indicator_id.in_(indicatorids)).all()
				if data:
					soildata=[plot,year,data]
					soildatas.append(soildata)
		return render_template('soil/_datas.html',datas=soildatas,indicators=indicators)
#	except:
#		return 'fail'


@bp.route("/indicator",methods=["GET","POST"])
@login_required
def indicator():
	if not current_user.check_roles(['admin','soil']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	form=SoilindicatorForm()
	form.indicatortype.choices=[('其它','其它'),('重金属','重金属'),('多环芳烃','多环芳烃')]
	if request.method=='POST' and (form.action.data is not None):
		if form.action.data==2:#action:  '1' for EDIT, '2' for 'DELETE'
			indicator=Soilindicator.query.filter_by(id=form.id.data).first()
			if indicator is None:
				flash('指标项删除失败！')
			else:
				for data in indicator.soildatas:
					db.session.delete(data)
				db.session.delete(indicator)
				db.session.commit()
				flash('土壤监测指标项 <{}> 删除成功！'.format(indicator.indicatorname))
		elif form.action.data==1:
			indicator=Soilindicator.query.filter_by(id=form.id.data).first()
			if indicator:
				indicator.symbol=form.symbol.data
				indicator.unit=form.unit.data
				indicator.dland_standard=form.dland_standard.data
				indicator.aland_standard_ph1=form.aland_standard_ph1.data
				indicator.aland_standard_ph2=form.aland_standard_ph2.data
				indicator.aland_standard_ph3=form.aland_standard_ph3.data
				indicator.aland_standard_ph4=form.aland_standard_ph4.data
				indicator.indicatortype=form.indicatortype.data
				db.session.commit()
				flash('土壤监测指标项 <{}> 编辑成功！'.format(indicator.indicatorname))
			else:
				flash('土壤监测指标项编辑失败！')
	indicators=Soilindicator.query.order_by(Soilindicator.indicatortype,Soilindicator.indicatorname).all()
	return render_template('soil/indicator.html',title='土壤监测指标项信息',indicators=indicators, form=form)


def check_indicators(sheet,workbook):
	added_indicators=[]
	for i in range(1,len(sheet.row_values(0))):
		indicators=sheet.row_values(0)[i].split()
		if indicators!="":
			indicator=Soilindicator.query.filter_by(indicatorname=indicators[0]).first()
			if indicator is None:
				indicator=Soilindicator(indicatorname=indicators[0])
				db.session.add(indicator)
				added_indicators.append(indicators[0])
				if len(indicators)>1:
					indicator.symbol=indicators[1]
				indicator.indicatortype='其它'
	if len(added_indicators)>0:
		db.session.commit()
	return added_indicators

def insert_soildatas(sheet,workbook,year):
	indicators=[]
	for i in range(1,len(sheet.row_values(0))):
		indicatornames=sheet.row_values(0)[i].split()
		indicator=Soilindicator.query.filter_by(indicatorname=indicatornames[0]).first()
		if indicator is None:
			return [-2,'系统找不到监测指标项 <{}> 的信息.'.format(indicatornames[0])]
		indicators.append(indicator)
	nrows=sheet.nrows
	newcount=0
	existcount=0
	for i in range(1,nrows):
		plotname=sheet.row_values(i)[0].strip(' ')
		plot=Soilplot.query.filter_by(plotname=plotname).first()
		if plot is None:
			return [-1,'系统中未找到样地<{}>的信息，请先添加该样地信息。'.format(plotname)]
		for j in range(1,len(indicators)+1):
			if sheet.cell(i,j).ctype==2:
				existdata=Soildata.query.filter_by(plot=plot).filter_by(year=year).filter_by(indicator=indicators[j-1]).first()
				if existdata:
					existcount=existcount+1
				else:
					data=Soildata(year=year,plot=plot,indicator=indicators[j-1],value=round(sheet.row_values(i)[j],2))
					db.session.add(data)
					newcount=newcount+1
	return [1,newcount,existcount]
				
