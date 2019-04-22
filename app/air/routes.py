import os
import json
from flask import render_template, flash, redirect, url_for, request, current_app, send_file, send_from_directory
from flask_login import current_user,login_required
from app import db
from app.air.forms import AirplotForm,VocQueryForm,DataQueryForm
from app.models import Airplot,Airdata,Voctype,Vocdata
from werkzeug.urls import url_parse
from werkzeug import secure_filename
import xlrd
import re
from datetime import date,datetime
from app.air import bp

ALLOWED_EXTENSIONS=set(['txt','pdf','png','jpg','jpeg','gif','xls','xlsx','csv'])

@bp.route('/airdata',methods=['GET','POST'])
@login_required
def airdata():
	if not current_user.check_roles(['admin','air']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	form=DataQueryForm()
	#form.plots.choices=[(item.plot.id,item.plot.plotname) for item in Airdata.query.group_by(Airdata.airplot_id).order_by(Airdata.airplot_id).all()]
	airdatas=Airdata.query.order_by(Airdata.airplot_id).all()
	form.plots.choices=[]
	existplot=None
	if len(airdatas)>0:
		existplot=airdatas[0].plot
		for item in airdatas:
			if item.plot!=existplot:
				form.plots.choices.append((existplot.id,existplot.plotname))
				existplot=item.plot
		form.plots.choices.append((existplot.id,existplot.plotname))
	form.plots.choices.insert(0,(-1,'全部'))
	datas=[]
	next_num=None
	prev_num=None
	pages=None
	current_page=1
	plotid=-1
	timestartstr=''
	timeendstr=''
	if request.method=='POST':
		if form.timestart.data.strip()=='':
			timestart=datetime(1990,1,1,0,0)
		else:
			timestart=datetime.strptime(form.timestart.data,'%Y-%m-%d %H:%M:%S')
		if form.timeend.data.strip()=='':
			timeend=datetime(4000,1,1,0,0)
		else:
			timeend=datetime.strptime(form.timeend.data,'%Y-%m-%d %H:%M:%S')
		page=request.args.get('page',1,type=int)
		if form.plots.data>=0:
			pagedatas=Airdata.query.filter(Airdata.airplot_id==form.plots.data,Airdata.timestamp>=timestart,Airdata.timestamp<=timeend).order_by(Airdata.timestamp).paginate(page,current_app.config['POSTS_PER_PAGE'],False)
		else:
			pagedatas=Airdata.query.filter(Airdata.timestamp>=timestart,Airdata.timestamp<=timeend).order_by(Airdata.timestamp).paginate(page,current_app.config['POSTS_PER_PAGE'],False)
		pages=pagedatas.pages
		current_page=pagedatas.page
		next_num=pagedatas.next_num if pagedatas.has_next else None
		prev_num=pagedatas.prev_num if pagedatas.has_prev else None
		datas=pagedatas.items
		plotid=form.plots.data
		timestartstr=form.timestart.data
		timeendstr=form.timeend.data
	return render_template('air/airdata.html',title='常规空气质量监测数据',datas=datas,next_num=next_num,prev_num=prev_num,form=form,plotid=plotid,timestart=timestartstr,timeend=timeendstr,pages=pages,current_page=current_page)

@bp.route('/airdatas',methods=['GET'])
@login_required
def airdatas():
	if not current_user.check_roles(['admin','air']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	page=request.args.get('page',1,type=int)
	startstr=request.args.get('timestart','',type=str)
	endstr=request.args.get('timeend','',type=str)
	plotid=request.args.get('plotid','-1',type=int)
	if startstr.strip()=='':
		timestart=datetime(1990,1,1,0,0)
	else:
		timestart=datetime.strptime(startstr,'%Y-%m-%d %H:%M:%S')
	if endstr.strip()=='':
		timeend=datetime(4000,1,1,0,0)
	else:
		timeend=datetime.strptime(endstr,'%Y-%m-%d %H:%M:%S')
	if plotid>=0:
		pagedatas=Airdata.query.filter(Airdata.airplot_id==plotid,Airdata.timestamp>=timestart,Airdata.timestamp<=timeend).order_by(Airdata.timestamp).paginate(page,current_app.config['POSTS_PER_PAGE'],False)
	else:
		pagedatas=Airdata.query.filter(Airdata.timestamp>=timestart,Airdata.timestamp<=timeend).order_by(Airdata.timestamp).paginate(page,current_app.config['POSTS_PER_PAGE'],False)
	pages=pagedatas.pages
	current_page=pagedatas.page
	next_num=pagedatas.next_num if pagedatas.has_next else None
	prev_num=pagedatas.prev_num if pagedatas.has_prev else None
	datas=pagedatas.items
	return render_template('air/_datas.html',datas=datas,next_num=next_num,prev_num=prev_num,pages=pages,current_page=current_page)

@bp.route('/editdata',methods=['POST'])
@login_required
def editdata():
	if not current_user.check_roles(['admin','air']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	try:	
		page=int(request.form['page'])
		startstr=request.form['timestart']
		endstr=request.form['timeend']
		plotid=int(request.form['plotid'])
		editid=request.form['editid']
		no2=request.form['no2']
		co=request.form['co']
		so2=request.form['so2']
		o3=request.form['o3']
		pm10=request.form['pm10']
		pm25=request.form['pm25']
		data=Airdata.query.filter_by(id=editid).first()
		if data is None:
			return 'fail'
		else:
			if no2.strip()=='':
				data.no2=None
			else:
				data.no2=int(no2)
			if so2.strip()=='':
				data.so2=None
			else:
				data.so2=int(so2)
			if o3.strip()=='':
				data.o3=None
			else:
				data.o3=int(o3)
			if pm10.strip()=='':
				data.pm10=None
			else:
				data.pm10=int(pm10)
			if pm25.strip()=='':
				data.pm25=None
			else:
				data.pm25=int(pm25)
			if co.strip()=='':
				data.co=None
			else:
				data.co=float(co) 
			db.session.commit()

			if startstr.strip()=='':
				timestart=datetime(1990,1,1,0,0)
			else:
				timestart=datetime.strptime(startstr,'%Y-%m-%d %H:%M:%S')
			if endstr.strip()=='':
				timeend=datetime(4000,1,1,0,0)
			else:
				timeend=datetime.strptime(endstr,'%Y-%m-%d %H:%M:%S')
			if plotid>=0:
				pagedatas=Airdata.query.filter(Airdata.airplot_id==plotid,Airdata.timestamp>=timestart,Airdata.timestamp<=timeend).order_by(Airdata.timestamp).paginate(page,current_app.config['POSTS_PER_PAGE'],False)
			else:
				pagedatas=Airdata.query.filter(Airdata.timestamp>=timestart,Airdata.timestamp<=timeend).order_by(Airdata.timestamp).paginate(page,current_app.config['POSTS_PER_PAGE'],False)
			pages=pagedatas.pages
			current_page=pagedatas.page
			next_num=pagedatas.next_num if pagedatas.has_next else None
			prev_num=pagedatas.prev_num if pagedatas.has_prev else None
			datas=pagedatas.items
			return render_template('air/_datas.html',datas=datas,next_num=next_num,prev_num=prev_num,pages=pages,current_page=current_page)
	except:
		return 'fail'


@bp.route('/deldata',methods=['POST'])
@login_required
def deldata():
	if not current_user.check_roles(['admin','air']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	try:	
		page=int(request.form['page'])
		startstr=request.form['timestart']
		endstr=request.form['timeend']
		plotid=int(request.form['plotid'])
		delid=request.form['delid']
		data=Airdata.query.filter_by(id=delid).first()
		if data is None:
			return 'fail'
		else:
			db.session.delete(data)
			db.session.commit()

			if startstr.strip()=='':
				timestart=datetime(1990,1,1,0,0)
			else:
				timestart=datetime.strptime(startstr,'%Y-%m-%d %H:%M:%S')
			if endstr.strip()=='':
				timeend=datetime(4000,1,1,0,0)
			else:
				timeend=datetime.strptime(endstr,'%Y-%m-%d %H:%M:%S')
			if plotid>=0:
				pagedatas=Airdata.query.filter(Airdata.airplot_id==plotid,Airdata.timestamp>=timestart,Airdata.timestamp<=timeend).order_by(Airdata.timestamp).paginate(page,current_app.config['POSTS_PER_PAGE'],False)
			else:
				pagedatas=Airdata.query.filter(Airdata.timestamp>=timestart,Airdata.timestamp<=timeend).order_by(Airdata.timestamp).paginate(page,current_app.config['POSTS_PER_PAGE'],False)
			pages=pagedatas.pages
			current_page=pagedatas.page
			next_num=pagedatas.next_num if pagedatas.has_next else None
			prev_num=pagedatas.prev_num if pagedatas.has_prev else None
			datas=pagedatas.items
			return render_template('air/_datas.html',datas=datas,next_num=next_num,prev_num=prev_num,pages=pages,current_page=current_page)
	except:
		return 'fail'

@bp.route('/vocdata',methods=['GET','POST'])
@login_required
def vocdata():
	if not current_user.check_roles(['admin','air']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	form=VocQueryForm()
	form.plots.choices=[(plot.id,plot.plotname) for plot in Airplot.query.order_by(Airplot.plotname).all()]
	form.voctypes.choices=[(voctype.id,voctype.vocname) for voctype in Voctype.query.order_by(Voctype.vocname).all()]
	#form.timestamps.choices=[(item.timestamp.strftime("%Y-%m-%d"),item.timestamp.strftime("%Y年%m月")) for item in Vocdata.query.group_by(Vocdata.timestamp).order_by(Vocdata.timestamp).all()]
	vocdatas=Vocdata.query.order_by(Vocdata.timestamp).all()
	form.timestamps.choices=[]
	existtime=None
	if len(vocdatas)>0:
		existtime=vocdatas[0].timestamp
		for item in vocdatas:
			if item.timestamp!=existtime:
				form.timestamps.choices.append((existtime.strftime("%Y-%m-%d"),existtime.strftime("%Y年%m月")))
				existtime=item.timestamp
		form.timestamps.choices.append((existtime.strftime("%Y-%m-%d"),existtime.strftime("%Y年%m月")))
	plots=[]	
	timestrs=[]
	voctypes=[]
	datas=[]
	if form.validate_on_submit():
		plots=Airplot.query.filter(Airplot.id.in_(form.plots.data)).all()		
		voctypes=Voctype.query.filter(Voctype.id.in_(form.voctypes.data)).all()
		times=[]
		for item in form.timestamps.data:
			times.append(datetime.strptime(item,"%Y-%m-%d"))
			timestrs.append(item)
		dataquery=Vocdata.query.filter(Vocdata.timestamp.in_(times),Vocdata.airplot_id.in_(form.plots.data),Vocdata.voctype_id.in_(form.voctypes.data)).order_by(Vocdata.timestamp,Vocdata.voctype_id)
		vocdatas=dataquery.all()
		datarow=[]
		if len(vocdatas)>0:
			datarow=[]
			voctype_id=vocdatas[0].voctype_id
			timestamp=vocdatas[0].timestamp
			for data in vocdatas:
				if voctype_id==data.voctype_id and timestamp==data.timestamp:
					datarow.append(data)
				else:
					datas.append(datarow)
					datarow=[]
					datarow.append(data)
					voctype_id=data.voctype_id
					timestamp=data.timestamp
		if len(datarow)>0:
			datas.append(datarow)
	return render_template('air/vocdata.html',title='挥发性有机物监测数据',form=form, plots=plots,datas=datas,timestrs=timestrs,voctypes=voctypes)

@bp.route('/delvocdata',methods=['POST'])
@login_required
def delvocdata():
	if not current_user.check_roles(['admin','air']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	try:
		plotid=request.form['plotid']
		time=request.form['time']
		typeid=request.form['typeid']
		plotids=request.form['plots']
		times=request.form['times']
		typeids=request.form['types']
		plotids=json.loads(plotids)
		timestrs=json.loads(times)
		typeids=json.loads(typeids)
		timestamp=datetime.strptime(time+'01日',"%Y年%m月%d日")
		if plotid=='0':
			datas=Vocdata.query.filter(Vocdata.voctype_id==typeid,Vocdata.timestamp==timestamp,Vocdata.airplot_id.in_(plotids)).all()
			if datas is None:
				return 'fail'
			else:
				for item in datas:
					db.session.delete(item)
				db.session.commit()
		else:
			data=Vocdata.query.filter(Vocdata.voctype_id==typeid,Vocdata.timestamp==timestamp,Vocdata.airplot_id==plotid).first()
			if data is None:
				return 'fail'
			else:
				db.session.delete(data)
				db.session.commit()
		datas=[]
		plots=Airplot.query.filter(Airplot.id.in_(plotids)).all()		
		times=[]
		for item in timestrs:
			times.append(datetime.strptime(item,"%Y-%m-%d"))
		dataquery=Vocdata.query.filter(Vocdata.timestamp.in_(times),Vocdata.airplot_id.in_(plotids),Vocdata.voctype_id.in_(typeids)).order_by(Vocdata.timestamp,Vocdata.voctype_id)
		vocdatas=dataquery.all()
		datarow=[]
		if len(vocdatas)>0:
			datarow=[]
			voctype_id=vocdatas[0].voctype_id
			timestamp=vocdatas[0].timestamp
			for data in vocdatas:
				if voctype_id==data.voctype_id and timestamp==data.timestamp:
					datarow.append(data)
				else:
					datas.append(datarow)
					datarow=[]
					datarow.append(data)
					voctype_id=data.voctype_id
					timestamp=data.timestamp
		if len(datarow)>0:
			datas.append(datarow)
		return render_template('air/_vocdatas.html',plots=plots,datas=datas)
	except:
		return 'fail'

@bp.route('/editvocdata',methods=['POST'])
@login_required
def editvocdata():
	if not current_user.check_roles(['admin','air']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	try:
		plotid=request.form['plotid']
		time=request.form['time']
		typeid=request.form['typeid']
		value=request.form['value']
		plotids=request.form['plots']
		times=request.form['times']
		typeids=request.form['types']
		plotids=json.loads(plotids)
		timestrs=json.loads(times)
		typeids=json.loads(typeids)
		timestamp=datetime.strptime(time+'01日',"%Y年%m月%d日")
		data=Vocdata.query.filter(Vocdata.voctype_id==typeid,Vocdata.timestamp==timestamp,Vocdata.airplot_id==plotid).first()
		if data is None:
			data=Vocdata(voctype_id=typeid,timestamp=timestamp,airplot_id=plotid,value=value)
			db.session.add(data)
		else:
			data.value=value
		db.session.commit()
		datas=[]
		plots=Airplot.query.filter(Airplot.id.in_(plotids)).all()		
		voctypes=Voctype.query.filter(Voctype.id.in_(typeids)).all()
		times=[]
		for item in timestrs:
			times.append(datetime.strptime(item,"%Y-%m-%d"))
		dataquery=Vocdata.query.filter(Vocdata.timestamp.in_(times),Vocdata.airplot_id.in_(plotids),Vocdata.voctype_id.in_(typeids)).order_by(Vocdata.timestamp,Vocdata.voctype_id)
		vocdatas=dataquery.all()
		datarow=[]
		if len(vocdatas)>0:
			datarow=[]
			voctype_id=vocdatas[0].voctype_id
			timestamp=vocdatas[0].timestamp
			for data in vocdatas:
				if voctype_id==data.voctype_id and timestamp==data.timestamp:
					datarow.append(data)
				else:
					datas.append(datarow)
					datarow=[]
					datarow.append(data)
					voctype_id=data.voctype_id
					timestamp=data.timestamp
		if len(datarow)>0:
			datas.append(datarow)
		return render_template('air/_vocdatas.html',plots=plots,datas=datas)
	except:
		return 'fail'

@bp.route('/voctype')
@login_required
def voctype():
	if not current_user.check_roles(['admin','air']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	voctypes=Voctype.query.order_by(Voctype.vocname).all()
	return render_template('air/voctype.html',title='挥发性有机物指标管理',voctypes=voctypes)

@bp.route('/editvoctype',methods=['POST'])
@login_required
def editvoctype():
	if not current_user.check_roles(['admin','air']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	try:
		typeid=request.form['typeid']
		typename=request.form['typename']
		if typename.strip()=='':
			return 'fail'
		else:
			voctype=Voctype.query.filter_by(id=typeid).first()
			if voctype:
				voctype.vocname=typename
				db.session.commit()
				voctypes=Voctype.query.order_by(Voctype.vocname).all()
				return render_template('air/_voctypes.html',voctypes=voctypes)
			else:
				return 'fail'			
	except:
		return 'fail'
	
@bp.route('/delvoctype',methods=['POST'])
@login_required
def delvoctype():
	if not current_user.check_roles(['admin','air']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	try:
		typeid=request.form['typeid']
		voctype=Voctype.query.filter_by(id=typeid).first()
		if voctype:
			for item in voctype.vocdatas:
				db.session.delete(item)
			db.session.delete(voctype)
			db.session.commit()
			voctypes=Voctype.query.order_by(Voctype.vocname).all()
			return render_template('air/_voctypes.html',voctypes=voctypes)
		else:
			return 'fail'			
	except:
		return 'fail'
							

@bp.route('/clearairdata')
@login_required
def clearairdata():
	if not current_user.check_roles(['admin','air']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	cleardata(Airdata)
	flash('已清空常规空气质量数据')
	return redirect(url_for('air.airdata'))
@bp.route('/clearvocdata')
@login_required
def clearvocdata():
	if not current_user.check_roles(['admin','air']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	cleardata(Vocdata)
	flash('已清空挥发性有机物数据')
	return redirect(url_for('air.vocdata'))

@bp.route('/clearvoctype')
@login_required
def clearvoctype():
	if not current_user.check_roles(['admin','air']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	cleardata(Voctype)
	flash('已清空VOC类型数据')
	return redirect(url_for('air.airdata'))

@bp.route('/upload',methods=['POST'])
@login_required
def upload():
	if not current_user.check_roles(['admin','air']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	table=[]
	info='No table now.'
	num=[]
	file=request.files['file']
	if file and allowed_file(file.filename):
		filename=secure_filename(file.filename)
		filepath=os.path.join(current_app.config['UPLOAD_FOLDER'],filename)
		file.save(filepath)
		workbook=xlrd.open_workbook(filepath)
		for sheetname in workbook.sheet_names():
			if sheetname.find('常规空气质量')>=0:
				(isinserted,info)=insert_routine_airdata(sheet=workbook.sheet_by_name(sheetname),workbook=workbook)
				if isinserted:
					flash(str.format('数据表 [{}] 上传成功！已添加常规空气监测数据 {} 条',sheetname,info))
				else:
					flash(str.format('数据表 [{}] 监测点位“{}”不存在，请先添加监测点位信息。本次未添加任何数据。',sheetname,info))
			elif sheetname.find('挥发性有机物')>=0:
				m=re.match(r'.+?(\d+)年(\d+)月.+',sheetname)
				if m:
					timestamp=datetime(2000+int(m.group(1)),int(m.group(2)),1)
					sheet=workbook.sheet_by_name(sheetname)
					if sheet.nrows>1:
						(newplots,plots)=get_plots(sheet.row_values(0))
						if len(newplots)>0:
							info=""
							for newplot in newplots:
								info=info+newplot+';'
							info=info.strip(';')
							flash(str.format("数据表 [{}] 监测点位“{}”不存在，请先添加监测点位信息。本次未添加任何数据。",sheetname,info))
						else:
							inserted_linenum=insert_vocdata(sheet,timestamp,plots)
							flash(str.format('数据表 [{}] 上传成功！已添加VOC监测数据 {} 条',sheetname,inserted_linenum))
					else:
						flash(str.format('数据表 [{}] 无数据，本次未添加任何数据。',sheetname))
				else:
					flash(str.format('数据表 [{}] 表名读取不到时间。本次未添加任何数据。',sheetname))
			else:
				continue
		return redirect(url_for('air.airdata'))
	else:
		flash('上传失败!')

@bp.route('/download_vocexample', methods=['GET'])
@login_required
def download_vocexample():
	if not current_user.check_roles(['admin','air']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	filename='airdata_example.xlsx'
	filepath=os.path.join(current_app.config['DOWNLOAD_FOLDER'])
	return send_from_directory(directory=filepath, filename=filename)


@bp.route("/plot",methods=["GET","POST"])
@login_required
def plot():
	if not current_user.check_roles(['admin','air']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	form=AirplotForm()
	if request.method=='POST' and (form.action.data is not None):
		if form.action.data==2:#action: '0' for ADD, '1' for EDIT, '2' for 'DELETE'
			plot=Airplot.query.filter_by(id=form.id.data).first()
			if plot is None:
				flash('点位删除失败！')
			else:
				for data in plot.airdatas:
					db.session.delete(data)
				for data in plot.vocdatas:
					db.session.delete(data)
				db.session.delete(plot)
				db.session.commit()
				flash('空气质量监测点位 <{}> 及其相关数据删除成功！'.format(plot.plotname))
		elif form.action.data==0:
			plot=Airplot(plotname=form.plotname.data,\
				landtype=form.landtype.data,\
				samplefrequency=form.samplefrequency.data,\
				latdegree=form.latdegree.data,\
				latminute=form.latminute.data,\
				latsecond=form.latsecond.data,\
				londegree=form.londegree.data,\
				lonminute=form.lonminute.data,\
				lonsecond=form.lonsecond.data)
			db.session.add(plot)
			db.session.commit()
			flash('空气质量监测点位 <{}> 添加成功！'.format(form.plotname.data))
		elif form.action.data==1:
			plot=Airplot.query.filter_by(id=form.id.data).first()
			if plot:
				plot.landtype=form.landtype.data
				plot.samplefrequency=form.samplefrequency.data
				plot.latdegree=form.latdegree.data
				plot.latminute=form.latminute.data
				plot.latsecond=form.latsecond.data
				plot.londegree=form.londegree.data
				plot.lonminute=form.lonminute.data
				plot.lonsecond=form.lonsecond.data
				db.session.commit()
				flash('空气质量监测点位 <{}> 编辑成功！'.format(form.plotname.data))
			else:
				flash('点位信息编辑失败！')
	plots=Airplot.query.order_by(Airplot.plotname).all()
	return render_template('air/airplots.html',title='空气质量监测站点管理',plots=plots, form=form)

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

def insert_routine_airdata(sheet,workbook):
	nrows=sheet.nrows
	airdatas=[]
	for i in range(2,nrows):
		row_values=sheet.row_values(i)
		plot=Airplot.query.filter_by(plotname=row_values[1].strip(' ')).first()
		if plot is None:
			return False,row_value[1]
		date_value=xlrd.xldate_as_tuple(row_values[0],workbook.datemode)
		timestamp=datetime(*date_value[:6])
		airdata=Airdata.query.filter(Airdata.airplot_id==plot.id,Airdata.timestamp==timestamp).first()
		if airdata is None:
			airdata=Airdata()
			db.session.add(airdata)
		airdata.plot=plot
		airdata.timestamp=timestamp
		if sheet.cell(i,2).ctype==2:
			airdata.co=row_values[2]
		if sheet.cell(i,3).ctype==2:
			airdata.no2=int(row_values[3])
		if sheet.cell(i,4).ctype==2:
			airdata.o3=int(row_values[4])
		if sheet.cell(i,5).ctype==2:
			airdata.so2=int(row_values[5])
		if sheet.cell(i,6).ctype==2:
			airdata.pm10=int(row_values[6])
		if sheet.cell(i,7).ctype==2:
			airdata.pm25=int(row_values[7])
	db.session.commit()
	return True,nrows-2

def insert_vocdata(sheet,timestamp,plots):
	count=0
	for i in range(1,sheet.nrows):
		vocname=sheet.row_values(i)[0]
		if vocname is None or vocname.strip()=='':
			continue
		vocname=vocname.strip()
		voctype=Voctype.query.filter_by(vocname=vocname).first()
		if voctype is None:
			voctype=Voctype(vocname=vocname)
			db.session.add(voctype)
		rowvalues=sheet.row_values(i)
		for j in range(0,len(plots)):
			if rowvalues[j+1] is None or rowvalues[j+1]=='':
				continue
			else:
				vocdata=Vocdata.query.filter(Vocdata.timestamp==timestamp,Vocdata.airplot_id==plots[j].id,Vocdata.voctype_id==voctype.id).first()
				if vocdata is None:
					vocdata=Vocdata(timestamp=timestamp,value=rowvalues[j+1],plot=plots[j],voctype=voctype)
					db.session.add(vocdata)
				else:
					vocdata.value=rowvalues[j+1]
				count=count+1
	db.session.commit()
	return count

def cleardata(dbmodel):
	datas=dbmodel.query.all()
	for data in datas:
		db.session.delete(data)
	db.session.commit()

def get_plots(rowvalues):
	newplots=[]
	plots=[]
	if len(rowvalues)>1:
		for i in range(1,len(rowvalues)):
			if rowvalues[i] is None or rowvalues[i].strip()=='':
				break
			plot=Airplot.query.filter_by(plotname=rowvalues[i].strip()).first()
			if plot is None:
				newplots.append(rowvalues[i].strip())
			else:
				plots.append(plot)
	return newplots,plots
