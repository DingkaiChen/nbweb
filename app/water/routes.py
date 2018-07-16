import os
from flask import render_template, flash, redirect, url_for, request, current_app
from app import db
from werkzeug.urls import url_parse
from werkzeug import secure_filename
import xlrd
import re
from datetime import date,datetime
from app.water import bp

ALLOWED_EXTENSIONS=set(['txt','pdf','png','jpg','jpeg','gif','xls','xlsx','csv'])

@bp.route("/water/data",methods=["GET","POST"])
def data():
	return render_template('water/data.html',title="水环境监测数据查询")
