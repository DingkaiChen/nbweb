from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField,SelectMultipleField, DateTimeField,DateField,SelectField
from wtforms.validators import DataRequired, InputRequired, ValidationError

class SoilplotForm(FlaskForm):
	id=IntegerField('ID')
	action=IntegerField('action')
	frequency=IntegerField('采样频率',validators=[DataRequired()])
	plotname=StringField('样地名称', validators=[DataRequired()])
	region=SelectField('区域', coerce=str,validators=[DataRequired()])
	latdegree=IntegerField('度',validators=[DataRequired()])
	latminute=IntegerField('分',validators=[DataRequired()])
	latsecond=FloatField('秒',validators=[InputRequired()])
	londegree=IntegerField('度',validators=[DataRequired()])
	lonminute=IntegerField('分',validators=[DataRequired()])
	lonsecond=FloatField('秒',validators=[InputRequired()])
	altitude=IntegerField('高程')
	submit=SubmitField('提交')

class SoildataqueryForm(FlaskForm):
	action=IntegerField('action')
	plots=SelectMultipleField('样地',coerce=int,validators=[DataRequired()])
	indicators=SelectMultipleField('指标',coerce=int,validators=[DataRequired()])
	years=SelectMultipleField('年份',coerce=int,validators=[DataRequired()])
	submit=SubmitField('查询')

class SoilindicatorForm(FlaskForm):
	id=IntegerField('ID')
	action=IntegerField('action')
	indicatorname=StringField('指标名称',validators=[DataRequired()])
	symbol=StringField('符号')
	unit=StringField('单位')
	dland_standard=FloatField('建设用地管控标准值')
	aland_standard_ph1=FloatField('PH<=5.5')
	aland_standard_ph2=FloatField('5.5&lt;PH<=6.5')
	aland_standard_ph3=FloatField('6.5&lt;PH<=7.5')
	aland_standard_ph4=FloatField('PH>=7.5')
	indicatortype=SelectField('指标类型')
	submit=SubmitField('提交')
	
