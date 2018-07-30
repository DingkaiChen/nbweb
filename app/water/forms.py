from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField,SelectMultipleField, DateTimeField,DateField,SelectField
from wtforms.validators import DataRequired, InputRequired, ValidationError

class WaterdataqueryForm(FlaskForm):
	plots=SelectMultipleField('点位',coerce=int,validators=[DataRequired()])
	indicators=SelectMultipleField('指标',coerce=int,validators=[DataRequired()])
	times=SelectMultipleField('时间',coerce=str,validators=[DataRequired()])
	tides=SelectMultipleField('潮位',coerce=str,validators=[DataRequired()])
	submit=SubmitField('查询')
