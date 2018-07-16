from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from app.models import User,Airplot,Forestplot,Waterplot,Soilplot
from app import db
from werkzeug.urls import url_parse
from app.main import bp

@bp.route('/')
@bp.route('/index')
def index():
	plots={}
	forestplots=Forestplot.query.all()
	soilplots=Soilplot.query.all()
	waterplots=Waterplot.query.all()
	airplots=Airplot.query.all()
	points=[]
	for plot in forestplots:
		lat=plot.latdegree+plot.latminute/60+plot.latsecond/3600
		lon=plot.londegree+plot.lonminute/60+plot.lonsecond/3600
		points.append({'lat':lat,'lon':lon})
	plots['forest']=points
	points=[]
	for plot in airplots:
		lat=plot.latdegree+plot.latminute/60+plot.latsecond/3600
		lon=plot.londegree+plot.lonminute/60+plot.lonsecond/3600
		points.append({'lat':lat,'lon':lon})
	plots['air']=points
	points=[]
	for plot in soilplots:
		lat=plot.latdegree+plot.latminute/60+plot.latsecond/3600
		lon=plot.londegree+plot.lonminute/60+plot.lonsecond/3600
		points.append({'lat':lat,'lon':lon})
	plots['soil']=points
	points=[]
	for plot in waterplots:
		lat=plot.latdegree+plot.latminute/60+plot.latsecond/3600
		lon=plot.londegree+plot.lonminute/60+plot.lonsecond/3600
		points.append({'lat':lat,'lon':lon})
	plots['water']=points
	return render_template('main/index.html', title='首页', plots=plots)

