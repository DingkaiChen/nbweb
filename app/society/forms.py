from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField,SelectMultipleField, DateTimeField,DateField,SelectField
from wtforms.validators import DataRequired, InputRequired, ValidationError

class SocietydataqueryForm(FlaskForm):
	action=IntegerField('action')
	indicators=SelectMultipleField('指标',coerce=int,validators=[DataRequired()])
	years=SelectMultipleField('年份',coerce=int,validators=[DataRequired()])
	submit=SubmitField('查询')

