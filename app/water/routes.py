import os
from flask import render_template, flash, redirect, url_for, request, current_app, send_file, send_from_directory
from app import db
from app.models import Watershed,Waterplot,Waterindicator,Waterdata
from app.water.forms import WaterdataqueryForm,WaterrealdataqueryForm
from werkzeug.urls import url_parse
from werkzeug import secure_filename
import xlrd
import re
import pymssql
from datetime import date,datetime,timedelta
from app.water import bp
from flask_login import current_user,login_required

ALLOWED_EXTENSIONS=set(['txt','pdf','png','jpg','jpeg','gif','xls','xlsx','csv'])

@bp.route("/watershed")
@login_required
def watershed():
	if not current_user.check_roles(['admin','water']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	datas=Watershed.query.order_by(Watershed.rivername).all()
	return render_template('water/watershed.html',title="流域项管理",datas=datas)

@bp.route("/addwatershed",methods=["POST"])
@login_required
def addwatershed():
	if not current_user.check_roles(['admin','water']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	try:
		rivername=request.form['rivername']
		data=Watershed.query.filter_by(rivername=rivername).first()
		if data:
			return 'fail1'
		else:
			data=Watershed(rivername=rivername)
			db.session.add(data)
			db.session.commit()
			datas=Watershed.query.order_by(Watershed.rivername).all()
			return render_template('water/_watersheds.html',datas=datas)
	except:
		return 'fail'

@bp.route("/editwatershed",methods=["POST"])
@login_required
def editwatershed():
	if not current_user.check_roles(['admin','water']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	try:
		watershedid=request.form['watershedid']
		rivername=request.form['rivername']
		data=Watershed.query.filter(Watershed.rivername==rivername,Watershed.id!=watershedid).first()
		if data:
			return 'fail1'
		else:
			data=Watershed.query.filter_by(id=watershedid).first()
			if data is None:
				return 'fail2'
			else:
				data.rivername=rivername
				db.session.commit()
				datas=Watershed.query.order_by(Watershed.rivername).all()
				return render_template('water/_watersheds.html',datas=datas)
	except:
		return 'fail'

@bp.route("/delwatershed",methods=["POST"])
@login_required
def delwatershed():
	if not current_user.check_roles(['admin','water']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	try:
		watershedid=request.form['watershedid']
		data=Watershed.query.filter_by(id=watershedid).first()
		if data is None:
			return 'fail1'
		else:
			db.session.delete(data)
			db.session.commit()
			datas=Watershed.query.order_by(Watershed.rivername).all()
			return render_template('water/_watersheds.html',datas=datas)
	except:
		return 'fail'

@bp.route("/plot")
@login_required
def plot():
	if not current_user.check_roles(['admin','water']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	watersheds=Watershed.query.order_by(Watershed.rivername).all()
	plots=Waterplot.query.order_by(Waterplot.plotname).all()
	return render_template('water/plot.html',title="水质监测点位管理",datas=plots,watersheds=watersheds)		

@bp.route("/addplot",methods=['POST'])
@login_required
def addplot():
	if not current_user.check_roles(['admin','water']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	plotname=request.form['plotname']
	plot=Waterplot.query.filter_by(plotname=plotname).first()
	if plot:
		return 'fail1'
	latdegree=request.form['latdegree']
	latminute=request.form['latminute']
	latsecond=request.form['latsecond']
	londegree=request.form['londegree']
	lonminute=request.form['lonminute']
	lonsecond=request.form['lonsecond']
	watershedid=request.form['watershedid']
	plot=Waterplot(watershed_id=watershedid,\
		plotname=plotname,\
		latdegree=latdegree,\
		latminute=latminute,\
		latsecond=latsecond,\
		londegree=londegree,\
		lonminute=lonminute,\
		lonsecond=lonsecond)
	db.session.add(plot)
	db.session.commit()
	plots=Waterplot.query.order_by(Waterplot.plotname).all()
	return render_template('water/_plots.html',datas=plots)		

@bp.route('/editplot',methods=['POST'])
@login_required
def editplot():
	if not current_user.check_roles(['admin','water']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	plotid=request.form['plotid']
	plotname=request.form['plotname']
	plot=Waterplot.query.filter(Waterplot.plotname==plotname,Waterplot.id!=plotid).first()
	if plot:
		return 'fail1'
	plot=Waterplot.query.filter_by(id=plotid).first()
	if plot is None:
		return 'fail2'
	latdegree=request.form['latdegree']
	latminute=request.form['latminute']
	latsecond=request.form['latsecond']
	londegree=request.form['londegree']
	lonminute=request.form['lonminute']
	lonsecond=request.form['lonsecond']
	plot.plotname=plotname
	plot.latdegree=latdegree
	plot.latminute=latminute
	plot.latsecond=latsecond
	plot.londegree=londegree
	plot.lonminute=lonminute
	plot.lonsecond=lonsecond
	db.session.commit()
	plots=Waterplot.query.order_by(Waterplot.plotname).all()
	return render_template('water/_plots.html',datas=plots)		

@bp.route('/delplot',methods=['POST'])
@login_required
def delplot():
	if not current_user.check_roles(['admin','water']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	plotid=request.form['plotid']
	plot=Waterplot.query.filter_by(id=plotid).first()
	if plot is None:
		return 'fail1'
	db.session.delete(plot)
	db.session.commit()
	plots=Waterplot.query.order_by(Waterplot.plotname).all()
	return render_template('water/_plots.html',datas=plots)		

@bp.route('/data',methods=['GET','POST'])
@login_required
def data():
	if not current_user.check_roles(['admin','water']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	form=WaterdataqueryForm()
	form.plots.choices=[(plot.id,'流域：{}，监测点：{}'.format(plot.watershed.rivername,plot.plotname)) for plot in Waterplot.query.order_by(Waterplot.watershed_id,Waterplot.plotname).all()]
	form.indicators.choices=[(indicator.id,'{}（{}）'.format(indicator.indicatorname,indicator.unit)) for indicator in Waterindicator.query.order_by(Waterindicator.indicatorname).all()]
	#form.times.choices=[(item.timestamp.strftime("%Y-%m-%d"),item.timestamp.strftime("%Y年%m月")) for item in Waterdata.query.group_by(Waterdata.timestamp).order_by(Waterdata.timestamp).all()]
	wdatas=Waterdata.query.order_by(Waterdata.timestamp).all()
	form.times.choices=[]
	existtime=None
	if len(wdatas)>0:
		existtime=wdatas[0].timestamp
		for item in wdatas:
			if item.timestamp!=existtime:
				form.times.choices.append((existtime.strftime("%Y-%m-%d"),existtime.strftime("%Y年%m月")))
				existtime=item.timestamp
		form.times.choices.append((existtime.strftime("%Y-%m-%d"),existtime.strftime("%Y年%m月")))
	#form.tides.choices=[(item.tide,item.tide) for item in Waterdata.query.group_by(Waterdata.tide).order_by(Waterdata.tide).all()]
	wdatas=Waterdata.query.order_by(Waterdata.tide).all()
	form.tides.choices=[]
	existtide=None
	if len(wdatas)>0:
		existtide=wdatas[0].tide
		for item in wdatas:
			if item.tide!=existtide:
				if existtide.strip(' ')=='':
					form.tides.choices.append((existtide,'（空）'))
				else:	
					form.tides.choices.append((existtide,existtide))
				existtide=item.tide
		if existtide.strip(' ')=='':
			form.tides.choices.append((existtide,'（空）'))
		else:	
			form.tides.choices.append((existtide,existtide))
	datas=[]
	indicators=[]
	plots=[]
	timestrs=[]
	tides=[]
	if request.method=='POST':
		if request.form['action']=='1':#'1':QUERY; '2':UPLOAD
			plots=Waterplot.query.filter(Waterplot.id.in_(form.plots.data)).order_by(Waterplot.plotname).all()
			indicators=Waterindicator.query.filter(Waterindicator.id.in_(form.indicators.data)).order_by(Waterindicator.id).all()
			tides=form.tides.data
			timestamps=[]
			for item in form.times.data:
				timestamps.append(datetime.strptime(item,"%Y-%m-%d"))
				timestrs.append(item)
			for plot in plots:
				for timestamp in timestamps:
					for tide in tides:
						data=Waterdata.query.filter(Waterdata.plot==plot,Waterdata.timestamp==timestamp,Waterdata.tide==tide,Waterdata.waterindicator_id.in_(form.indicators.data)).all()
						if len(data)>0:
							waterdata=[plot,timestamp.strftime("%Y年%m月"),tide,data[0].weather,data]
							datas.append(waterdata)
		elif request.form['action']=='2':
			file=request.files['file']
			if file and allowed_file(file.filename):
				filename=secure_filename(file.filename)
				filepath=os.path.join(current_app.config['UPLOAD_FOLDER'],filename)
				file.save(filepath)
				workbook=xlrd.open_workbook(filepath)
				hassheet=False
				for sheetname in workbook.sheet_names():
					added_indicators=check_indicators(sheet=workbook.sheet_by_name(sheetname),workbook=workbook)
					if len(added_indicators)>0:
						flash('已添加指标项 {} 共{}项'.format('，'.join(added_indicators),len(added_indicators)))
					result=insert_waterdatas(sheet=workbook.sheet_by_name(sheetname),workbook=workbook)
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
					form.indicators.choices=[(indicator.id,'{}（{}）'.format(indicator.indicatorname,indicator.unit)) for indicator in Waterindicator.query.order_by(Waterindicator.indicatorname).all()]
					#form.times.choices=[(item.timestamp.strftime("%Y-%m-%d"),item.timestamp.strftime("%Y年%m月")) for item in Waterdata.query.group_by(Waterdata.timestamp).order_by(Waterdata.timestamp).all()]
					wdatas=Waterdata.query.order_by(Waterdata.timestamp).all()
					form.times.choices=[]
					existtime=None
					if len(wdatas)>0:
						existtime=wdatas[0].timestamp
						for item in wdatas:
							if item.timestamp!=existtime:
								form.times.choices.append((existtime.strftime("%Y-%m-%d"),existtime.strftime("%Y年%m月")))
								existtime=item.timestamp
						form.times.choices.append((existtime.strftime("%Y-%m-%d"),existtime.strftime("%Y年%m月")))
					#form.tides.choices=[(item.tide,item.tide) for item in Waterdata.query.group_by(Waterdata.tide).order_by(Waterdata.tide).all()]
					wdatas=Waterdata.query.order_by(Waterdata.tide).all()
					form.tides.choices=[]
					existtide=None
					if len(wdatas)>0:
						existtide=wdatas[0].tide
						for item in wdatas:
							if item.tide!=existtide:
								form.tides.choices.append((existtide,existtide))
								existtide=item.tide
						form.tides.choices.append((existtide,existtide))
				if hassheet==False:
					flash('文件中未找到数据表，请上传规范格式的文件，具体请参考模板。')
			else:
				flash('出错：请上传规范格式的文件，具体请参考模板。')
	return render_template('water/data.html',title="水质调查数据管理",form=form,datas=datas,indicators=indicators,plots=plots,timestrs=timestrs,tides=tides)

@bp.route('/realdata',methods=['GET','POST'])
@login_required
def realdata():
	if not current_user.check_roles(['admin','water']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	server='dnuedatabase1.sqlserver.rds.aliyuncs.com:3433'
	user='webuser'
	password='WebUser#2015'
	database='nbwater_iot'
	conn=pymssql.connect(server,user,password,database)
	cursor=conn.cursor()
	form=WaterrealdataqueryForm()
	form.plots.choices=[]
	cursor.execute('select id,plotname from plot')
	row=cursor.fetchone()
	while row:
		form.plots.choices.append((row[0],row[1]))
		row=cursor.fetchone()
	conn.close()
	time1=datetime.now()
	time0=time1+timedelta(days=-1)
	timestartstr=time0.strftime('%Y-%m-%d %H:%M:%S')
	timeendstr=time1.strftime('%Y-%m-%d %H:%M:%S')
	datas=[]
	if request.method=='POST':
		if form.timestart.data.strip()!='':
			timestartstr=form.timestart.data
		if form.timeend.data.strip()!='':
			timeendstr=form.timeend.data
		if form.plots.data:
			plotid=form.plots.data
			try:
				timestart=datetime.strptime(timestartstr,'%Y-%m-%d %H:%M:%S')
				timeend=datetime.strptime(timeendstr,'%Y-%m-%d %H:%M:%S')
				conn=pymssql.connect(server,user,password,database)
				cursor=conn.cursor()
				cursor.execute("select dt,temp,ph,ORP,spCond,sal,depth,turbidity,LDO from data where dt>='{}' and dt<='{}' order by dt".format(timestartstr,timeendstr))
				row=cursor.fetchone()
				while row:
					datas.append((row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]))
					row=cursor.fetchone()
			finally:
				conn.close()
	else:
		form.timestart.data=timestartstr
		form.timeend.data=timeendstr
	return render_template('water/realdata.html',title='水环境物联网监测数据',form=form,datas=datas)

@bp.route('/download_dataexample', methods=['GET'])
@login_required
def download_dataexample():
	if not current_user.check_roles(['admin','water']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	filename='waterdata_example.xlsx'
	filepath=os.path.join(current_app.config['DOWNLOAD_FOLDER'])
	return send_from_directory(directory=filepath, filename=filename)

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

def check_indicators(sheet,workbook):
	added_indicators=[]
	for i in range(6,len(sheet.row_values(0))):
		indstr=sheet.row_values(0)[i].strip()
		if indstr!="":
			m1=re.match(r'(.+)\((.+)\)',indstr)
			if m1:
				name=m1.group(1)
				unit=m1.group(2)
			else:
				name=indstr
				unit=""
			indicator=Waterindicator.query.filter(Waterindicator.indicatorname==name,Waterindicator.unit==unit).first()
			if indicator is None:
				indicator=Waterindicator(indicatorname=name,unit=unit)
				db.session.add(indicator)
				added_indicators.append(name)
	if len(added_indicators)>0:
		db.session.commit()
	return added_indicators

def insert_waterdatas(sheet,workbook):
	indicators=[]
	for i in range(6,len(sheet.row_values(0))):
		indstr=sheet.row_values(0)[i].strip()
		name=""
		unit=""
		if indstr!="":
			m1=re.match(r'(.+)\((.+)\)',indstr)
			if m1:
				name=m1.group(1)
				unit=m1.group(2)
			else:
				name=indstr
		else:
			return [-2,'存在空白指标名称']
		indicator=Waterindicator.query.filter(Waterindicator.indicatorname==name,Waterindicator.unit==unit).first()
		if indicator is None:
			return [-2,'系统找不到监测指标项 <{}> 的信息.'.format(name)]
		else:
                	indicators.append(indicator)
	nrows=sheet.nrows
	newcount=0
	existcount=0
	for i in range(1,nrows):
		plotname=sheet.row_values(i)[1].strip(' ')
		plot=Waterplot.query.filter_by(plotname=plotname).first()
		if plot is None:
			return [-1,'系统中未找到监测点位<{}>的信息，请先添加该点位信息。'.format(plotname)]
		year=sheet.row_values(i)[2]
		month=sheet.row_values(i)[3]
		timestamp=datetime(1999,1,1)
		try:
			timestamp=datetime(int(year),int(month),1)
		except:
			return [-1,'年度和月份数据格式不正确']
		tide=sheet.row_values(i)[4].strip(' ')
		weather=sheet.row_values(i)[5].strip(' ')
		for j in range(6,len(indicators)+6):
			if sheet.cell(i,j).ctype==2:
				existdata=Waterdata.query.filter(Waterdata.plot==plot,Waterdata.timestamp==timestamp,Waterdata.tide==tide,Waterdata.indicator==indicators[j-6]).first()
				if existdata:
					existcount=existcount+1
				else:
					data=Waterdata(plot=plot,timestamp=timestamp,weather=weather,tide=tide,indicator=indicators[j-6],value=round(sheet.row_values(i)[j],3))
					db.session.add(data)
					newcount=newcount+1
	return [1,newcount,existcount]

