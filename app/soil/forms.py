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
	indicatortype=SelectField('指标类型')
	submit=SubmitField('提交')
	
