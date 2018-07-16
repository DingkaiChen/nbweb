import os
import json
from app.soil.forms import SoilplotForm,SoildataqueryForm
from app.models import Soilplot,Soilindicator,Soildata
from flask import render_template, flash, redirect, url_for, request, current_app, send_file, send_from_directory
from app import db
from werkzeug.urls import url_parse
from werkzeug import secure_filename
import xlrd
import re
from datetime import date,datetime
from app.soil import bp

ALLOWED_EXTENSIONS=set(['txt','pdf','png','jpg','jpeg','gif','xls','xlsx','csv'])

@bp.route("/plot",methods=["GET","POST"])
def plot():
	form=SoilplotForm()
	form.region.choices=[('北仑城区网格化采样','北仑城区网格化采样'),('城郊乡梯度流域采样','城郊乡梯度流域采样')]
	if request.method=='POST' and form.action.data:
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
def clearplots():
	cleardata(Soilplot)
	flash('已清空土壤调查样地数据')
	return redirect(url_for('soil.plot'))

@bp.route('/download_plotexample', methods=['GET'])
def download_plotexample():
	filename='soilplots_example.xlsx'
	filepath=os.path.join(current_app.config['DOWNLOAD_FOLDER'])
	return send_from_directory(directory=filepath, filename=filename)

@bp.route('/download_dataexample', methods=['GET'])
def download_dataexample():
	filename='soildatas_example.xlsx'
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
	try:
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
	except:
		return -1

@bp.route('/data',methods=['GET','POST'])
def data():
	form=SoildataqueryForm()
	form.plots.choices=[(plot.id,plot.plotname) for plot in Soilplot.query.all()]
	form.years.choices=[(item.year,str(item.year)) for item in Soildata.query.group_by(Soildata.year).all()]
	form.indicators.choices=[(indicator.id,indicator.indicatorname) for indicator in Soilindicator.query.all()]
	soildatas=[]
	if request.method=='POST' and form.action.data:
		if form.action.data==0:#action: '0' for EXCEL FILE UPLOAD, '1' for QUERY, '2' for 'DELETE', '3' for excel file upload
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
						if len(added_indicators>0):
							flash('已添加指标项 {} 共{}项'.format(added_indicators.join('，'),len(added_indicators)))
						result=insert_soildatas(sheet=workbook.sheet_by_name(sheetname),workbook=workbook,year)
						if result>0:
							db.session.commit()
							flash('数据上传完成，已成功添加数据 {} 条'.format(str(result)))
						elif result==0:
							flash('数据上传完成，未添加任何数据')
						else:
							flash('数据上传失败')
						hassheet=True
				if hassheet==False:
					flash('上传文件中未找到以年份命名的数据表。请上传规范格式的文件，具体请参考模板。')
			else:
				flash('出错：请上传规范格式的文件，具体请参考模板。')
		elif form.action.data==1:
			plots=Soilplot.query.filter(Soilplot.id.in_(form.plots.data)).all()
			indicators=Soilindicator.query.filter(Soilindicator.id.in_(form.indicators.data)).all()
			years=form.years.data
			soildatas=Soildata.query.filter(Soildata.soilplot_id.in_(form.plots.data),Soildata.soilindicator_id.in_(form.indicators.data),Soildata.year.in_(form.years.data)).all()
	return render_template('soil/data.html',title='土壤调查数据',form=form,datas=soildatas)
	"""
	years=[sample.year for sample in Soildata.query.group_by(Soildata.year).order_by(Soildata.year.desc()).all()]
	if request.method=="GET":
		year=request.args.get('year')
	
	quadrats=Herbquadrat.query.filter_by(forestplot_id=plotid).order_by(Herbquadrat.number).all()
	if len(quadrats)==0:
		flash('指定样地无样方信息，请先添加样方.')
		return redirect(url_for('forest.plot'))
	else:
		quadrat=quadrats[0]
		herbsample=None
		if len(times)>0:
			if time is None:
				time=times[0]
			timestamp=datetime.strptime(time,'%Y-%m-%d')
			herbsample=Herbsample.query.filter(Herbsample.quadrat==quadrat,Herbsample.timestamp==timestamp).first()
		herbsampleform=HerbsampleForm()
		herbform=HerbForm()
		herbform.herbtype.choices=[(herbtype.id,herbtype.chnname) for herbtype in Herbtype.query.order_by(Herbtype.chnname.desc()).all()]
		return render_template('forest/herb.html',title='草本植物调查数据',times=times,time=time,quadrats=quadrats,quadrat=quadrat,herbsample=herbsample,herbsampleform=herbsampleform,herbform=herbform)
	"""
@bp.route('/delyear',methods=['POST'])
def delyear():
	year=int(request.form['year'])
	datas=Soildata.query.filter_by(year=year).all()
	for data in datas:
		db.session.delete(data)
	db.session.commit()
	return redirect(url_for('soil.data',plotid=plotid))

def check_indicators(sheet,workbook):
	added_indicators=[]
	for i in range(1,len(sheet.row_values(0))):
		indicators=sheet.row_values(0)[i].split()
		if indicators!="":
			indicator=Soilindicator.query.filter_by(indicatorname=indicator[0]).first()
			if indicator is None:
				indicator=Soilindicator(indicatorname==indicator[0])
				db.session.add(indicator)
				added_indicators.append(indicator[0])
				if len(indicators)>1:
					indicator.symbol=indicator[1]
	if len(added_indicators)>0:
		db.session.commit()
	return added_indicators

def insert_soildatas(sheet,workbook,year):
	indicators=[]
	for i in range(1,len(sheet.row_values(0))):
		indicatornames=sheet.row_values(0)[i].split()
		indicator=Soilindicator.query.filter_by(indicatorname=indicatornames[0]).first()
		if indicator is None:
			return -2
		indicators.append(indicator)
	nrows=sheet.nrows
	count=0
	for i in range(1,nrows):
		plot=Soilplot.query.filter_by(plotname=sheet.row_values(i)[0].strip(' '))
		if plot is None:
			return -1
		for j in range(1,len(indicators)+1):
			if sheet.cell(i,j).ctype==2:
				data=Soildata(year=year,plot=plot,indicator=indicators[j-1],value=sheet.row_values(i)[j])
				db.session.add(data)
				count=count+1
	return count
				
