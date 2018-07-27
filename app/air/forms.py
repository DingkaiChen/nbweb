from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField,SelectField,SelectMultipleField, DateTimeField,DateField
from wtforms.validators import DataRequired, InputRequired, ValidationError
class AirplotForm(FlaskForm):
	id=IntegerField('ID')
	action=IntegerField('action')
	samplefrequency=StringField('采样频率',validators=[DataRequired()])
	plotname=StringField('点位名称', validators=[DataRequired()])
	landtype=StringField('区域功能类型', validators=[DataRequired()])
	latdegree=IntegerField('度',validators=[DataRequired()])
	latminute=IntegerField('分',validators=[DataRequired()])
	latsecond=FloatField('秒',validators=[InputRequired()])
	londegree=IntegerField('度',validators=[DataRequired()])
	lonminute=IntegerField('分',validators=[DataRequired()])
	lonsecond=FloatField('秒',validators=[InputRequired()])
	submit=SubmitField('提交')

class VocQueryForm(FlaskForm):
	voctypes=SelectMultipleField('选择挥发性有机物类型',coerce=int,validators=[DataRequired()])
	plots=SelectMultipleField('选择监测点位',coerce=int,validators=[DataRequired()])
	timestamps=SelectMultipleField('监测时间',coerce=str,validators=[DataRequired()])
	submit=SubmitField('查询')

class DataQueryForm(FlaskForm):
	plots=SelectField('监测点',coerce=int,validators=[DataRequired()])
	timestart=StringField('开始时间',validators=[DataRequired()])
	timeend=StringField('结束时间',validators=[DataRequired()])
	submit=SubmitField('查询')
