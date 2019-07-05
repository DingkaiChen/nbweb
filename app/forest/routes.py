import os
import json 
from flask import render_template, flash, redirect, url_for, request, current_app
from app.forest.forms import ForestplotForm,ArborsampleForm,ArborForm,ArbortypeForm,QuadratForm,HerbtypeForm,HerbsampleForm,HerbForm
from app.models import Forestplot,Arbor,Arborsample,Arbortype,Herbquadrat,Herbsample,Herbtype,Herb
from app import db
from werkzeug.urls import url_parse
from werkzeug import secure_filename
import xlrd
import re
from datetime import date,datetime
from app.forest import bp
from flask_login import current_user,login_required

ALLOWED_EXTENSIONS=set(['txt','pdf','png','jpg','jpeg','gif','xls','xlsx','csv'])

@bp.route("/plot",methods=["GET","POST"])
@login_required
def plot():
	if not current_user.check_roles(['admin','forest']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	form=ForestplotForm()
	if form.validate_on_submit():
		if form.id.data==0:
			plot=Forestplot(plotname=form.plotname.data,\
				address=form.address.data,\
				latdegree=form.latdegree.data,\
				latminute=form.latminute.data,\
				latsecond=form.latsecond.data,\
				londegree=form.londegree.data,\
				lonminute=form.lonminute.data,\
				lonsecond=form.lonsecond.data,\
				altitude=form.altitude.data,\
				imgurl=form.imgurl.data)
			db.session.add(plot)
			db.session.commit()
			flash('植被调查样地添加成功！')
		else:
			plot=Forestplot.query.filter_by(id=form.id.data).first()
			if plot:
				plot.address=form.address.data
				plot.latdegree=form.latdegree.data
				plot.latminute=form.latminute.data
				plot.latsecond=form.latsecond.data
				plot.londegree=form.londegree.data
				plot.lonminute=form.lonminute.data
				plot.lonsecond=form.lonsecond.data
				plot.altitude=form.altitude.data
				plot.imgurl=form.imgurl.data
				db.session.commit()
				flash('样地 "{}" 编辑成功！'.format(form.plotname.data))
			else:
				flash('样地数据编辑失败！')
	plots=Forestplot.query.all()
	splots=[]
	for plot in plots:
		arbors_count=len(plot.arbors.all())
		quadrats_count=len(plot.quadrats.all())
		splots.append([plot,arbors_count,quadrats_count])
	return render_template('forest/plot.html',title='植被调查样地信息',plots=splots, form=form)
		
@bp.route("/delplot",methods=["POST"])
@login_required
def delplot():
	if not current_user.check_roles(['admin','forest']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	plotid=request.form['id']
	name=request.form['name']
	plot=Forestplot.query.filter_by(id=plotid).first()
	if plot is None:
		return 'fail'
	else:
		for arbor in plot.arbors:
			for arborsample in arbor.samples:
				db.session.delete(arborsample)
			db.session.delete(arbor)
		db.session.delete(plot)
		db.session.commit()
		plots=Forestplot.query.all()
		splots=[]
		for plot in plots:
			arbors_count=len(plot.arbors.all())
			quadrats_count=len(plot.quadrats.all())
			splots.append([plot,arbors_count,quadrats_count])
		return render_template('forest/_plots.html',plots=splots)

@bp.route("/arborsample",methods=["GET","POST"])
@login_required
def arborsample():
	if not current_user.check_roles(['admin','forest']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	plotid=request.args.get('plotid')
	time=request.args.get('time')
	plot=Forestplot.query.filter_by(id=plotid).first()
	if plot is None:
		flash('查询样地数据不存在！')
		return redirect(url_for("forest.plot"))
	form=ArborsampleForm()
	form.arbor.choices=[(arbor.id,'编号{}：{}'.format(arbor.number-arbor.plot.id*1000000,arbor.arbortype.chnname)) for arbor in Arbor.query.filter_by(plot=plot).order_by(Arbor.number).all()]
	if form.validate_on_submit():
		if form.id.data==0:
			arbor=Arbor.query.filter_by(id=form.arbor.data).first()
			timestamp=datetime.strptime(str(form.timestamp.data),'%Y-%m-%d')
			arborsample=Arborsample.query.filter(Arborsample.arbor_id==arbor.id,Arborsample.timestamp==timestamp).first()
			if arborsample:
				flash('数据已存在，添加失败！')
			else:
				arborsample=Arborsample(arbor=arbor,timestamp=timestamp,\
					canopy_side1=form.canopyside1.data,\
					canopy_side2=form.canopyside2.data,\
					diameter=form.diameter.data,\
					height=form.height.data,\
					note=form.note.data)
				db.session.add(arborsample)
				db.session.commit()
				flash('数据添加成功')
		else:
			timestamp=datetime.strptime(str(form.timestamp.data),'%Y-%m-%d')
			arborsample=Arborsample.query.filter(Arborsample.arbor_id==form.arbor.data,Arborsample.timestamp==timestamp).first()
			if arborsample:
				arborsample.canopy_side1=form.canopyside1.data
				arborsample.canopy_side2=form.canopyside2.data
				arborsample.diameter=form.diameter.data
				arborsample.height=form.height.data
				arborsample.note=form.note.data
				db.session.commit()
				flash('数据编辑成功.')
			else:
				flash('数据编辑失败.')
		time=str(form.timestamp.data)
	arborids=[arbor.id for arbor in plot.arbors]
	#samples_bytime=Arborsample.query.filter(Arborsample.arbor_id.in_(arborids)).group_by(Arborsample.timestamp).order_by(Arborsample.timestamp.desc()).all()
	asamples=Arborsample.query.filter(Arborsample.arbor_id.in_(arborids)).order_by(Arborsample.timestamp.desc()).all()
	times=[]
	etime=None
	if len(asamples)>0:
		etime=asamples[0].timestamp
		for item in asamples:
			if item.timestamp!=etime:
				times.append(etime.strftime('%Y-%m-%d'))
				etime=item.timestamp
		times.append(etime.strftime('%Y-%m-%d'))
	samples=[]
	if time:
		timestamp=datetime.strptime(time,'%Y-%m-%d')
		samples=Arborsample.query.join(Arborsample.arbor).filter(Arborsample.arbor_id.in_(arborids),Arborsample.timestamp==timestamp).order_by(Arbor.number).all()
	else:
		if len(times)>0:
			timestamp=datetime.strptime(times[0],'%Y-%m-%d')
			time=times[0]
			samples=Arborsample.query.filter(Arborsample.arbor_id.in_(arborids),Arborsample.timestamp==timestamp).join(Arborsample.arbor).order_by(Arbor.number).all()		
		else:
			time=""
	return render_template('forest/arborsample.html',form=form,plot=plot,time=time,samples=samples,times=times,title="乔木采样数据")

@bp.route("/delarborsample",methods=["POST"])
@login_required
def delarborsample():
	if not current_user.check_roles(['admin','forest']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	sampleid=request.form['id']
	delsample=Arborsample.query.filter_by(id=sampleid).first()
	if delsample is None:
		return 'fail'
	else:
		timestamp=delsample.timestamp
		arborids=[arbor.id for arbor in delsample.arbor.plot.arbors]
		db.session.delete(delsample)
		db.session.commit()
		samples=Arborsample.query.join(Arborsample.arbor).filter(Arborsample.arbor_id.in_(arborids),Arborsample.timestamp==timestamp).order_by(Arbor.number).all()
		return render_template('forest/_arborsamples.html',samples=samples)
	
@bp.route("/arbortype",methods=["GET","POST"])
@login_required
def arbortype():
	if not current_user.check_roles(['admin','forest']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	form=ArbortypeForm()
	if form.validate_on_submit():
		if form.id.data==0:
			existtype=Arbortype.query.filter_by(chnname=form.chnname.data).first()
			if existtype:
				flash('树种名“{}”已存在，数据添加失败！'.format(form.chnname.data))
			else:
				arbortype=Arbortype(chnname=form.chnname.data,\
					latinname=form.latinname.data,\
					imgurl=form.imgurl.data)
				db.session.add(arbortype)
				db.session.commit()
				flash('树种 <{}> 添加成功！'.format(arbortype.chnname))
		else:
			existtype=Arbortype.query.filter(Arbortype.chnname==form.chnname.data, Arbortype.id!=form.id.data).first()
			if existtype:
				flash('树种名“{}”已存在，数据修改失败！'.format(form.chnname.data))
			else:
				arbortype=Arbortype.query.filter_by(id=form.id.data).first()
				if arbortype:
					arbortype.chnname=form.chnname.data
					arbortype.latinname=form.latinname.data
					arbortype.imgurl=form.imgurl.data
					db.session.commit()
					flash('树种 <{}> 数据修改成功！'.format(arbortype.chnname))
				else:
					flash('树种数据修改失败！')
	arbortypes=Arbortype.query.order_by(Arbortype.chnname).all()
	return render_template('forest/arbortype.html',title="树种数据管理",form=form,typedatas=arbortypes)

@bp.route("/delarbortype",methods=["POST"])
@login_required
def delarbortype():
	if not current_user.check_roles(['admin','forest']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	typeid=request.form['id']
	name=request.form['name']
	arbortype=Arbortype.query.filter_by(id=typeid).first()
	if arbortype is None:
		return 'fail'
	else:
		for arbor in arbortype.arbors:
			for arborsample in arbor.samples:
				db.session.delete(arborsample)
			db.session.delete(arbor)
		db.session.delete(arbortype)
		db.session.commit()
		arbortypes=Arbortype.query.order_by(Arbortype.chnname).all()
		return render_template('forest/_typedatas.html',typedatas=arbortypes)

@bp.route("/imgupload",methods=["POST"])
@login_required
def imgupload():
	if not current_user.check_roles(['admin','forest']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	file=request.files['file1']
	msg=""
	error=""
	imgurl=""
	if file and allowed_file(file.filename):
		filename=secure_filename(file.filename)
		filepath=os.path.join(current_app.config['IMG_FOLDER'],filename)
		file.save(filepath)
		msg="成功！文件大小为："+str(os.path.getsize(filepath));
		imgurl="../static/imgs/"+filename;
	jsonstr=json.dumps({'error':error,'msg':msg,'imgurl':imgurl})
	return jsonstr

@bp.route("/arbor/<plotid>",methods=["GET","POST"])
@login_required
def arbor(plotid):
	if not current_user.check_roles(['admin','forest']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	plot=Forestplot.query.filter_by(id=plotid).first()
	if plot is None:
		flash('查询样地数据不存在！')
		return redirect(url_for("forest.plot"))
	else:
		form=ArborForm()
		form.chnname.choices=[(arbortype.id,arbortype.chnname) for arbortype in Arbortype.query.order_by(Arbortype.chnname).all()]
		if form.validate_on_submit():
			if form.id.data==0:#Add
				existarbor=Arbor.query.filter(Arbor.number==form.number.data+plot.id*1000000,Arbor.plot==plot).first()
				if existarbor is None:
					arbortype=Arbortype.query.filter_by(id=form.chnname.data).first()
					if arbortype:
						arbor=Arbor(arbortype=arbortype,
							plot=plot,
							number=form.number.data+plot.id*1000000)
						db.session.add(arbor)
						db.session.commit()
						flash('树种数据 <编号：{}> 添加成功！'.format(form.number.data))
					else:
						flash('树种类型不存在，添加失败.')
				else:
					flash('树种编号<{}>已存在，添加失败。'.format(str(form.number.data)))
			else:#Edit
				arbortype=Arbortype.query.filter_by(id=form.chnname.data).first()
				if arbortype:
					arbor=Arbor.query.filter(Arbor.number==form.number.data+plot.id*1000000,Arbor.plot==plot).first()
					if arbor:
						arbor.arbortype=arbortype
						db.session.commit()
						flash('树种数据 <编号：{}> 修改成功。'.format(form.number.data))
					else:
						flash('树种数据 <编号：{}> 编号不存在，修改失败。'.format(form.number.data))
				else:
					flash('树种类型不存在，数据修改失败.')
		arbors=Arbor.query.filter(Arbor.plot==plot).order_by(Arbor.number).all()
		return render_template('forest/arbor.html',title="样地乔木数据管理",plot=plot,arbors=arbors,form=form)

@bp.route("/arbor/delarbor",methods=["POST"])
@login_required
def delarbor():
	if not current_user.check_roles(['admin','forest']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	number=request.form['number']
	plotid=request.form['plotid']
	plot=Forestplot.query.filter_by(id=plotid).first()
	if plot is None:
		return 'fail'
	else:
		arbor=Arbor.query.filter(Arbor.number==number+plot.id*1000000,Arbor.plot==plot).first()
		if arbor is None:
			return 'fail'
		else:
			for arborsample in arbor.samples:
				db.session.delete(arborsample)
			db.session.delete(arbor)
			db.session.commit()
			arbors=Arbor.query.filter(Arbor.plot==plot).order_by(Arbor.number).all()
			return render_template('forest/_arbors.html',plot=plot,arbors=arbors)

@bp.route("/quadrat",methods=["GET","POST"])
@login_required
def quadrat():
	if not current_user.check_roles(['admin','forest']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	form=QuadratForm()
	form.plot.choices=[(plot.id,plot.plotname) for plot in Forestplot.query.all()]
	if form.validate_on_submit():
		number=form.number.data
		existquadrat=Herbquadrat.query.filter(Herbquadrat.number==number,Herbquadrat.forestplot_id==form.plot.data).first()
		if existquadrat:
			flash('样地 <{}> 已存在样方编号 <{}>，样方添加失败.'.format(existquadrat.plot.plotname,str(number)))
		else:
			quadrat=Herbquadrat(number=number,forestplot_id=form.plot.data)
			db.session.add(quadrat)
			db.session.commit()
			flash('样方 <编号：{}> 已成功添加至样地 <{}>'.format(str(number),quadrat.plot.plotname))
	quadrats=Herbquadrat.query.join(Herbquadrat.plot).order_by(Forestplot.plotname,Herbquadrat.number).all()
	return render_template('forest/quadrat.html',title='样方管理',quadrats=quadrats,form=form)

@bp.route('/delquadrat',methods=['POST'])
@login_required
def delquadrat():
	if not current_user.check_roles(['admin','forest']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	del_id=request.form['id']
	quadrat=Herbquadrat.query.filter_by(id=del_id).first()
	if quadrat:
		db.session.delete(quadrat)
		db.session.commit()
		quadrats=Herbquadrat.query.join(Herbquadrat.plot).order_by(Forestplot.plotname,Herbquadrat.number).all()
		return render_template('forest/_quadrats.html',quadrats=quadrats)
	else:
		return 'fail'

@bp.route("/herbtype",methods=["GET","POST"])
@login_required
def herbtype():
	if not current_user.check_roles(['admin','forest']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	form=HerbtypeForm()
	if form.validate_on_submit():
		if form.id.data==0:
			existtype=Herbtype.query.filter_by(chnname=form.chnname.data).first()
			if existtype:
				flash('草本植物种名“{}”已存在，数据添加失败！'.format(form.chnname.data))
			else:
				herbtype=Herbtype(chnname=form.chnname.data,\
					latinname=form.latinname.data,\
					imgurl=form.imgurl.data)
				db.session.add(herbtype)
				db.session.commit()
				flash('草本植物 <{}> 添加成功！'.format(herbtype.chnname))
		else:
			existtype=Herbtype.query.filter(Herbtype.chnname==form.chnname.data, Herbtype.id!=form.id.data).first()
			if existtype:
				flash('草本植物种名“{}”已存在，数据修改失败！'.format(form.chnname.data))
			else:
				herbtype=Herbtype.query.filter_by(id=form.id.data).first()
				if herbtype:
					herbtype.chnname=form.chnname.data
					herbtype.latinname=form.latinname.data
					herbtype.imgurl=form.imgurl.data
					db.session.commit()
					flash('草本植物 <{}> 数据修改成功！'.format(herbtype.chnname))
				else:
					flash('草本植物数据修改失败！')
	herbtypes=Herbtype.query.order_by(Herbtype.chnname).all()
	return render_template('forest/herbtype.html',title="草本植物种类管理",form=form,typedatas=herbtypes)

@bp.route("/delherbtype",methods=["POST"])
@login_required
def delherbtype():
	if not current_user.check_roles(['admin','forest']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	typeid=request.form['id']
	name=request.form['name']
	herbtype=Herbtype.query.filter_by(id=typeid).first()
	if herbtype is None:
		return 'fail'
	else:
		db.session.delete(herbtype)
		db.session.commit()
		herbtypes=Herbtype.query.order_by(Herbtype.chnname).all()
		return render_template('forest/_typedatas.html',typedatas=herbtypes)

@bp.route('/herb',methods=['GET','POST'])
@login_required
def herb():
	if not current_user.check_roles(['admin','forest']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	#times=[sample.timestamp.strftime('%Y-%m-%d') for sample in Herbsample.query.group_by(Herbsample.timestamp).order_by(Herbsample.timestamp.desc()).all()]
	hsamples=Herbsample.query.order_by(Herbsample.timestamp.desc()).all()
	times=[]
	etime=None
	if len(hsamples)>0:
		etime=hsamples[0].timestamp
		for item in hsamples:
			if item.timestamp!=etime:
				times.append(etime.strftime('%Y-%m-%d'))
				etime=item.timestamp
		times.append(etime.strftime('%Y-%m-%d'))
	if request.method=="GET":
		plotid=request.args.get('plotid')
		time=request.args.get('time')
	else:
		plotid=request.form['plotid']
		time=request.form['time']
		times.append(time)
		flash('调查日期<{}>添加成功.'.format(time))
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

@bp.route('/delherbtime',methods=['POST'])
@login_required
def delherbtime():
	if not current_user.check_roles(['admin','forest']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	plotid=request.form['plotid']
	time=request.form['time']
	timestamp=datetime.strptime(time,'%Y-%m-%d')
	quadratsamples=Herbsample.query.join(Herbsample.quadrat).filter(Herbsample.timestamp==timestamp,Herbquadrat.forestplot_id==plotid).all()
	for quadratsample in quadratsamples:
		for herbsample in quadratsample.herbs:
			db.session.delete(herbsample)
		db.session.delete(quadratsample)
	db.session.commit()
	return redirect(url_for('forest.herb',plotid=plotid))

@bp.route('/changetab',methods=['GET'])
@login_required
def changetab():
	if not current_user.check_roles(['admin','forest']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	quadratid=request.args.get('quadratid')
	quadrat=Herbquadrat.query.filter_by(id=quadratid).first()
	if quadrat is None:
		return 'fail'
	time=request.args.get('time')
	quadrats=Herbquadrat.query.filter_by(forestplot_id=quadrat.forestplot_id).order_by(Herbquadrat.number).all()
	if len(quadrats)==0:
		return 'fail'
	else:
		herbsample=None
		timestamp=datetime.strptime(time,'%Y-%m-%d')
		quadratsample=Herbsample.query.filter(Herbsample.quadrat==quadrat,Herbsample.timestamp==timestamp).first()
		return render_template('forest/_quadratsamples.html',quadrats=quadrats,quadrat=quadrat,herbsample=quadratsample)
	
@bp.route('/editquadratsample',methods=['POST'])
@login_required
def editquadratsample():#add or edit quadrat sample
	if not current_user.check_roles(['admin','forest']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	sample_id=request.form['sample_id']
	quadrat_id=request.form['quadrat_id']
	time=request.form['time']
	greenstructure=request.form['greenstructure']
	herbcoverage=request.form['herbcoverage']
	arborstructure=request.form['arborstructure']
	sampletype=request.form['sampletype']
	if sample_id=="0":
		quadrat=Herbquadrat.query.filter_by(id=quadrat_id).first()
		if quadrat is None:
			return 'fail'
		else:
			quadratsample=Herbsample(quadrat=quadrat,\
				timestamp=datetime.strptime(time,'%Y-%m-%d'),\
				greenstructure=greenstructure,\
				herbcoverage=herbcoverage,\
				arborstructure=arborstructure,\
				sampletype=sampletype)
			db.session.add(quadratsample)
			db.session.commit()
	else:
		quadratsample=Herbsample.query.filter_by(id=sample_id).first()
		if quadratsample is None:
			return 'fail@编辑失败：找不到指定的样方数据.'
		else:
			quadratsample.greenstructure=greenstructure
			quadratsample.herbcoverage=herbcoverage
			quadratsample.arborstructure=arborstructure
			quadratsample.sampletype=sampletype
			db.session.commit()
	return render_template('forest/_quadratsample.html',herbsample=quadratsample)

@bp.route('/delquadratsample',methods=['POST'])
@login_required
def delquadratsample():
	if not current_user.check_roles(['admin','forest']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	sample_id=request.form['id']
	quadratsample=Herbsample.query.filter_by(id=sample_id).first()
	if quadratsample is None:
		return 'fail@删除失败：找不到指定的样方调查数据.'
	else:
		for herbsample in quadratsample.herbs:
			db.session.delete(herbsample)
		db.session.delete(quadratsample)
		db.session.commit()
		return	'<span>所选调查时间内没有数据，</span><a href="#" data-toggle="modal" data-target="#addsampleModal">添加数据？</a>'

@bp.route('/editherbsample',methods=['POST'])
@login_required
def editherbsample():#add or edit herbsample data
	if not current_user.check_roles(['admin','forest']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	herbtype_id=request.form['herbtype']
	herbsample_id=request.form['herbsample_id']
	quantity=request.form['quantity']
	height=request.form['height']
	coverage=request.form['coverage']
	state=request.form['state']
	phenology=request.form['phenology']
	herb_id=request.form['id']
	if herb_id=="0":
		herbsample=Herbsample.query.filter_by(id=herbsample_id).first()
		herbtype=Herbtype.query.filter_by(id=herbtype_id).first()
		if herbsample is None:
			return 'fail@添加失败：找不到指定的样方调查数据'
		elif herbtype is None:
			return 'fail@添加失败：所选草本植被不存在'
		elif Herb.query.filter(Herb.herbtype_id==herbtype_id,Herb.herbsample_id==herbsample_id).first():
			return 'fail@添加失败：草本植被<{}>数据已存在'.format(herbtype.chnname)
		else:
			herb=Herb(sample=herbsample,\
				herbtype=herbtype,\
				quantity=quantity,\
				height=height,\
				coverage=coverage,\
				state=state,\
				phenology=phenology)
			db.session.add(herb)
			db.session.commit()
	else:
		herb=Herb.query.filter_by(id=herb_id).first()
		if herb is None:
			return 'fail@编辑失败：找不到指定的草本数据'
		else:
			herb.quantity=quantity
			herb.height=height
			herb.coverage=coverage
			herb.state=state
			herb.phenology=phenology
			db.session.commit()
			herbsample=herb.sample
	return render_template('forest/_herbsinsample.html',herbsample=herbsample)

@bp.route('/delherbsample',methods=['POST'])
@login_required
def delherbsample():
	if not current_user.check_roles(['admin','forest']):
		flash('您无权访问该页面')
		return redirect(url_for('main.index'))
	herb_id=request.form['id']
	herb=Herb.query.filter_by(id=herb_id).first()
	if herb is None:
		return 'fail@删除失败：找不到指定的草本植被数据'
	else:
		herbsample=herb.sample
		db.session.delete(herb)
		db.session.commit()
		return render_template('forest/_herbsinsample.html',herbsample=herbsample)
	
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS
