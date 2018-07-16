from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField,SelectMultipleField, DateTimeField,DateField,SelectField
from wtforms.validators import DataRequired, InputRequired, ValidationError

class ForestplotForm(FlaskForm):
	id=IntegerField('ID')
	plotname=StringField('样地名称', validators=[DataRequired()])
	address=StringField('详细地址')
	latdegree=IntegerField('度',validators=[DataRequired()])
	latminute=IntegerField('分',validators=[DataRequired()])
	latsecond=FloatField('秒',validators=[InputRequired()])
	londegree=IntegerField('度',validators=[DataRequired()])
	lonminute=IntegerField('分',validators=[DataRequired()])
	lonsecond=FloatField('秒',validators=[InputRequired()])
	altitude=IntegerField('高程')
	submit=SubmitField('提交')

class ArbortypeForm(FlaskForm):
	id=IntegerField('ID')
	chnname=StringField('种名',validators=[DataRequired()])
	latinname=StringField('拉丁名')
	imgurl=StringField('图片')
	submit=SubmitField('提交')

class ArborForm(FlaskForm):
	id=IntegerField('ID')
	number=IntegerField('编号',validators=[InputRequired()])
	chnname=SelectField('种名',coerce=int,validators=[DataRequired()])
	submit=SubmitField('提交')

class ArborsampleForm(FlaskForm):
	id=IntegerField('ID')
	timestamp=DateField('调查时间',validators=[DataRequired()])
	arbor=SelectField('树木',coerce=int,validators=[DataRequired()])
	canopyside1=FloatField('冠幅边长1',validators=[])
	canopyside2=FloatField('冠幅边长2',validators=[])
	diameter=FloatField('胸径',validators=[])
	height=FloatField('树高',validators=[])
	note=StringField('备注',validators=[])
	submit=SubmitField('提交')

class QuadratForm(FlaskForm):
	id=IntegerField('ID')
	plot=SelectField('样地',coerce=int,validators=[DataRequired()])
	number=IntegerField('样方编号',validators=[DataRequired()])
	submit=SubmitField('提交')

class HerbtypeForm(FlaskForm):
	id=IntegerField('ID')
	chnname=StringField('种名',validators=[DataRequired()])
	latinname=StringField('拉丁名')
	imgurl=StringField('图片')
	submit=SubmitField('提交')

class HerbsampleForm(FlaskForm):
	id=IntegerField('ID')
	greenstructure=StringField('绿地结构')
	herbcoverage=StringField('草本植物总盖度')
	arborstructure=StringField('样方上方乔灌结构')
	sampletype=StringField('样点类型')

class HerbForm(FlaskForm):
	id=IntegerField('ID')
	herbtype=SelectField('名称',coerce=int,validators=[DataRequired()])
	herbsample_id=IntegerField('herbsample_id')
	quantity=StringField('株数',validators=[InputRequired()])
	height=IntegerField('高度',validators=[DataRequired()])
	coverage=IntegerField('盖度',validators=[InputRequired()])
	state=StringField('生活状况')
	phenology=StringField('物侯')	
