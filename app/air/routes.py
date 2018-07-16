import os
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user,login_required
from app import db
from app.air.forms import AirplotForm,VocQueryForm
from app.models import Airplot,Airdata,Voctype,Vocdata
from werkzeug.urls import url_parse
from werkzeug import secure_filename
import xlrd
import re
from datetime import date,datetime
from app.air import bp

ALLOWED_EXTENSIONS=set(['txt','pdf','png','jpg','jpeg','gif','xls','xlsx','csv'])

@bp.route('/air/airdata',methods=['GET','POST'])
def airdata():
	page=request.args.get('page',1,type=int)
	datas=Airdata.query.paginate(page,current_app.config['POSTS_PER_PAGE'],False)
	next_url=url_for('air.airdata',page=datas.next_num) if datas.has_next else None
	prev_url=url_for('air.airdata',page=datas.prev_num) if datas.has_prev else None
	return render_template('air/airdata.html',title='常规空气质量监测数据',datas=datas.items,next_url=next_url,prev_url=prev_url)

@bp.route('/air/vocdata',methods=['GET','POST'])
def vocdata():
	form=VocQueryForm()
	form.plots.choices=[(plot.id,plot.plotname) for plot in Airplot.query.all()]
	form.voctypes.choices=[(voctype.id,voctype.vocname) for voctype in Voctype.query.all()]
	plots=[]	
	datas=[]
	next_url=None
	prev_url=None
	if form.validate_on_submit():
		plots=Airplot.query.filter(Airplot.id.in_(form.plots.data)).all()		
		voctypes=Voctype.query.filter(Voctype.id.in_(form.voctypes.data)).all()
		timestart=datetime.strptime(str(form.starttime.data),'%Y-%m-%d')
		timeend=datetime.strptime(str(form.endtime.data),'%Y-%m-%d')
		page=request.args.get('page',1,type=int)
		dataquery=Vocdata.query.filter(Vocdata.timestamp>=timestart,Vocdata.timestamp<=timeend,Vocdata.airplot_id.in_(form.plots.data),Vocdata.voctype_id.in_(form.voctypes.data))
		month=dataquery.group_by(Vocdata.timestamp).order_by(Vocdata.timestamp,Vocdata.voctype_id).paginate(page,1,False)
		next_url=url_for('air.vocdata',page=month.next_num) if month.has_next else None
		prev_url=url_for('air.vocdata',page=month.prev_num) if month.has_prev else None
		vocdatas=dataquery.all()
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
	return render_template('air/vocdata.html',title='挥发性有机物监测数据',form=form, plots=plots,datas=datas,next_url=next_url,prev_url=prev_url)

@bp.route('/clearairdata')
def clearairdata():
	cleardata(Airdata)
	flash('已清空常规空气质量数据')
	return redirect(url_for('air.airdata'))
@bp.route('/clearvocdata')
def clearvocdata():
	cleardata(Vocdata)
	flash('已清空挥发性有机物数据')
	return redirect(url_for('air.vocdata'))

@bp.route('/clearvoctype')
def clearvoctype():
	cleardata(Voctype)
	flash('已清空VOC类型数据')
	return redirect(url_for('air.airdata'))

@bp.route('/upload',methods=['GET','POST'])
def upload():
	table=[]
	info='No table now.'
	num=[]
	if request.method=='POST':
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
	return render_template('air/upload.html',title='上传', table=table,info=info,num=num)

@bp.route('/airplots',methods=['GET','POST'])
def airplots():
	form=AirplotForm()
	if form.validate_on_submit():
		plot=Airplot(plotname=form.plotname.data,\
			landtype=form.landtype.data,\
			latdegree=form.latdegree.data,\
			latminute=form.latminute.data,\
			latsecond=form.latsecond.data,\
			londegree=form.londegree.data,\
			lonminute=form.lonminute.data,\
			lonsecond=form.lonsecond.data,\
			samplefrequency=form.samplefrequency.data)
		db.session.add(plot)
		db.session.commit()
		flash('空气质量监测点添加成功!')
	plots=Airplot.query.all()
	return render_template('air/airplots.html',title='空气质量监测站点',plots=plots, form=form)

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

def insert_routine_airdata(sheet,workbook):
	nrows=sheet.nrows
	airdatas=[]
	for i in range(2,nrows):
		airdata=Airdata()
		row_values=sheet.row_values(i)
		plot=Airplot.query.filter_by(plotname=row_values[1].strip(' ')).first()
		if plot is None:
			return False,row_value[1]
		date_value=xlrd.xldate_as_tuple(row_values[0],workbook.datemode)
		timestamp=datetime(*date_value[:6])
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
		db.session.add(airdata)
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
				vocdata=Vocdata(timestamp=timestamp,value=rowvalues[j+1],plot=plots[j],voctype=voctype)
				db.session.add(vocdata)
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
