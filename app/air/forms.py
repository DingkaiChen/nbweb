from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField,SelectMultipleField, DateTimeField,DateField
from wtforms.validators import DataRequired, InputRequired, ValidationError

class AirplotForm(FlaskForm):
	plotname=StringField('站点名称', validators=[DataRequired()])
	landtype=StringField('区域功能类型')
	latdegree=IntegerField('度',validators=[DataRequired()])
	latminute=IntegerField('分',validators=[DataRequired()])
	latsecond=FloatField('秒',validators=[InputRequired()])
	londegree=IntegerField('度',validators=[DataRequired()])
	lonminute=IntegerField('分',validators=[DataRequired()])
	lonsecond=FloatField('秒',validators=[InputRequired()])
	altitude=IntegerField('高程')
	samplefrequency=StringField('采样频率', validators=[DataRequired()])
	submit=SubmitField('添加')

class VocQueryForm(FlaskForm):
	voctypes=SelectMultipleField('选择挥发性有机物类型',coerce=int,validators=[DataRequired()])
	plots=SelectMultipleField('选择监测点位',coerce=int,validators=[DataRequired()])
	starttime=DateField('开始时间',validators=[DataRequired()])
	endtime=DateField('结束时间', validators=[DataRequired()])
	submit=SubmitField('查询')
