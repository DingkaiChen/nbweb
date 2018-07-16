import os
from flask import render_template, flash, redirect, url_for, request, current_app
from app import db
from werkzeug.urls import url_parse
from werkzeug import secure_filename
import xlrd
import re
from datetime import date,datetime
from app.map import bp

@bp.route("/map",methods=["GET","POST"])
def map():
	return render_template('map/map.html',title="监测点位分布图")
