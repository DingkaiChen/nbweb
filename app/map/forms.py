from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField,SelectMultipleField, DateTimeField,DateField,SelectField
from wtforms.validators import DataRequired, InputRequired, ValidationError

class SoilshpForm(FlaskForm):
	id=IntegerField('ID')
	action=IntegerField('action')
	indicators=SelectField('指标',coerce=int,validators=[DataRequired()])
	regions=SelectField('区域',coerce=str,validators=[DataRequired()])
	years=SelectField('年份',coerce=int,validators=[DataRequired()])
	shp=StringField('地图服务地址',validators=[DataRequired()])
	submit=SubmitField('提交')
