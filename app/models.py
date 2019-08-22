from app import db,login
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from time import time
from datetime import datetime
import jwt

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

roles_users=db.Table('roles_users',\
	db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
	db.Column('role_id',db.Integer,db.ForeignKey('role.id')))

class Role(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	rolename=db.Column(db.String(64),unique=True)
	description=db.Column(db.String(255))

class User(UserMixin, db.Model):
	id=db.Column(db.Integer, primary_key=True)
	username=db.Column(db.String(64), index=True, unique=True)
	email=db.Column(db.String(120), index=True, unique=True)
	password_hash=db.Column(db.String(128))
	posts=db.relationship('Post', backref='author', lazy='dynamic')
	roles=db.relationship('Role',\
		secondary=roles_users,\
		backref=db.backref('users',lazy='dynamic'))
	name=db.Column(db.String(64))
	phone=db.Column(db.String(32))

	def __repr__(self):
		return '<User {}>'.format(self.username)

	def set_password(self,password):
		self.password_hash=generate_password_hash(password)

	def check_password(self,password):
		return check_password_hash(self.password_hash,password)

	def check_roles(self,rolenames):
		for rolename in rolenames:
			role=Role.query.filter_by(rolename=rolename).first()
			if role in self.roles:
				return True
		return False
	
	def get_reset_password_token(self,expires_in=600):
		return jwt.encode(\
			{'reset_password':self.id,'exp':time()+expires_in},\
			current_app.config['SECRET_KEY'],algorithm='HS256').decode('utf-8')

	@staticmethod
	def verify_reset_password_token(token):
		try:
			id=jwt.decode(token,current_app.config['SECRET_KEY'],algorithms=['HS256'])['reset_password']
		except:
			return
		return User.query.get(id)

class Register(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(64),index=True,unique=True)
	email=db.Column(db.String(120),index=True,unique=True)
	password_hash=(db.Column(db.String(128)))
	name=db.Column(db.String(64))
	phone=db.Column(db.String(32))
	verified=db.Column(db.Integer)

	def __repr__(self):
		return '<Register {}>'.format(self.username)

	def set_password(self,password):
		self.password_hash=generate_password_hash(password)
	
	def verify(self):
		self.verified=1

	def get_register_verify_token(self,expires_in=600):
		return jwt.encode(\
			{'register_verify':self.id,'exp':time()+expires_in},\
			current_app.config['SECRET_KEY'],algorithm='HS256').decode('utf-8')

	@staticmethod
	def verify_register_verify_token(token):
		try:
			id=jwt.decode(token,current_app.config['SECRET_KEY'],algorithms=['HS256'])['register_verify']
		except:
			return
		return Register.query.get(id)


class Post(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	body=db.Column(db.String(140))
	timestamp=db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id=db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post {}>'.format(self.body)

class Airplot(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	plotname=db.Column(db.String(50))
	latdegree=db.Column(db.Integer)
	latminute=db.Column(db.Integer)
	latsecond=db.Column(db.Float)
	londegree=db.Column(db.Integer)
	lonminute=db.Column(db.Integer)
	lonsecond=db.Column(db.Float)
	altitude=db.Column(db.Integer)
	landtype=db.Column(db.String(50))
	samplefrequency=db.Column(db.String(20))
	airdatas=db.relationship('Airdata',backref='plot', lazy='dynamic')	
	vocdatas=db.relationship('Vocdata',backref='plot', lazy='dynamic')
	
	def __repr__(self):
		return '<Airplot {}>'.format(self.plotname)	

class Voctype(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	vocname=db.Column(db.String(50))
	vocdatas=db.relationship('Vocdata',backref='voctype',lazy='dynamic')

	def __repr__(self):
		return '<Voctype {}>'.format(self.vocname)

class Airdata(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	timestamp=db.Column(db.DateTime, index=True, default=datetime.utcnow)
	co=db.Column(db.Float)
	no2=db.Column(db.Integer)
	o3=db.Column(db.Integer)
	so2=db.Column(db.Integer)
	pm10=db.Column(db.Integer)
	pm25=db.Column(db.Integer)
	airplot_id=db.Column(db.Integer, db.ForeignKey('airplot.id'))

class Vocdata(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	timestamp=db.Column(db.DateTime, index=True, default=datetime.utcnow)
	value=db.Column(db.Float)
	voctype_id=db.Column(db.Integer, db.ForeignKey('voctype.id'))
	airplot_id=db.Column(db.Integer, db.ForeignKey('airplot.id'))

class Watershed(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	rivername=db.Column(db.String(50), index=True, unique=True)
	plots=db.relationship('Waterplot',backref='watershed',lazy='dynamic')

	def __repr__(self):
		return '<Watershed {}>'.format(self.rivername)

class Waterplot(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	plotname=db.Column(db.String(50))
	latdegree=db.Column(db.Integer)
	latminute=db.Column(db.Integer)
	latsecond=db.Column(db.Float)
	londegree=db.Column(db.Integer)
	lonminute=db.Column(db.Integer)
	lonsecond=db.Column(db.Float)
	altitude=db.Column(db.Integer)
	watershed_id=db.Column(db.Integer, db.ForeignKey('watershed.id'))
	waterdatas=db.relationship('Waterdata',backref='plot',lazy='dynamic')
	
	def __repr__(self):
		return '<Waterplot {}>'.format(self.plotname)	

class Waterindicator(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	indicatorname=db.Column(db.String(50),index=True,unique=True)
	symbol=db.Column(db.String(50))
	unit=db.Column(db.String(50))
	waterdatas=db.relationship('Waterdata',backref='indicator',lazy='dynamic')

	def __repr__(self):
		return '<Waterindicator {}>'.format(self.indicatorname)

class Waterdata(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	timestamp=db.Column(db.DateTime, index=True, default=datetime.utcnow)
	samplename=db.Column(db.String(50))
	weather=db.Column(db.String(50))
	tide=db.Column(db.String(50))
	value=db.Column(db.Float)
	waterplot_id=db.Column(db.Integer,db.ForeignKey('waterplot.id'))
	waterindicator_id=db.Column(db.Integer,db.ForeignKey('waterindicator.id'))

class Forestplot(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	plotname=db.Column(db.String(50))
	address=db.Column(db.String(50))
	latdegree=db.Column(db.Integer)
	latminute=db.Column(db.Integer)
	latsecond=db.Column(db.Float)
	londegree=db.Column(db.Integer)
	lonminute=db.Column(db.Integer)
	lonsecond=db.Column(db.Float)
	altitude=db.Column(db.Integer)
	imgurl=db.Column(db.String(120))
	arbors=db.relationship('Arbor',backref='plot',lazy='dynamic')
	quadrats=db.relationship('Herbquadrat',backref='plot',lazy='dynamic')

	def __repr__(self):
		return '<Forestplot {}>'.format(self.plotname)
	
class Herbquadrat(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	number=db.Column(db.Integer)
	note=db.Column(db.String(120))
	forestplot_id=db.Column(db.Integer,db.ForeignKey('forestplot.id'))
	samples=db.relationship('Herbsample',backref='quadrat',lazy='dynamic')
	
	def __repr__(self):
		return '<Hearquadrat {}>'.format(str(self.number))

class Herbsample(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	timestamp=db.Column(db.DateTime, index=True, default=datetime.utcnow)
	greenstructure=db.Column(db.String(50))
	herbcoverage=db.Column(db.Integer)
	arborstructure=db.Column(db.String(50))
	sampletype=db.Column(db.String(50))
	herbquadrat_id=db.Column(db.Integer,db.ForeignKey('herbquadrat.id'))
	herbs=db.relationship('Herb',backref='sample',lazy='dynamic')
	
class Herbtype(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	chnname=db.Column(db.String(50),index=True,unique=True)
	latinname=db.Column(db.String(50))
	imgurl=db.Column(db.String(120))
	herbs=db.relationship('Herb',backref='herbtype',lazy='dynamic')

	def __repr__(self):
		return '<Herbtype {}>'.format(self.chnname)

class Herb(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	herbtype_id=db.Column(db.Integer,db.ForeignKey('herbtype.id'))
	herbsample_id=db.Column(db.Integer,db.ForeignKey('herbsample.id'))
	quantity=db.Column(db.String(20))
	height=db.Column(db.Integer)
	coverage=db.Column(db.Integer)
	state=db.Column(db.String(50))
	phenology=db.Column(db.String(50))

class Arbortype(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	chnname=db.Column(db.String(50),index=True,unique=True)
	latinname=db.Column(db.String(50))
	imgurl=db.Column(db.String(120))
	arbors=db.relationship('Arbor',backref='arbortype',lazy='dynamic')

	def __repr__(self):
		return '<Arbortype {}>'.format(self.chnname)

class Arbor(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	number=db.Column(db.Integer,index=True,unique=True)
	arbortype_id=db.Column(db.Integer,db.ForeignKey('arbortype.id'))
	forestplot_id=db.Column(db.Integer,db.ForeignKey('forestplot.id'))
	samples=db.relationship('Arborsample',backref='arbor',lazy='dynamic')

class Arborsample(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	arbor_id=db.Column(db.Integer,db.ForeignKey('arbor.id'))
	timestamp=db.Column(db.DateTime, index=True, default=datetime.utcnow)
	quantity=db.Column(db.Integer,default=1)
	canopy_side1=db.Column(db.Float)
	canopy_side2=db.Column(db.Float)
	diameter=db.Column(db.Float)
	height=db.Column(db.Float)
	note=db.Column(db.String(120))

class Soilplot(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	plotname=db.Column(db.String(50))
	latdegree=db.Column(db.Integer)
	latminute=db.Column(db.Integer)
	latsecond=db.Column(db.Float)
	londegree=db.Column(db.Integer)
	lonminute=db.Column(db.Integer)
	lonsecond=db.Column(db.Float)
	altitude=db.Column(db.Integer)
	region=db.Column(db.String(50))
	frequency=db.Column(db.Integer)
	soildatas=db.relationship('Soildata',backref='plot',lazy='dynamic')
	
	def __repr__(self):
		return '<Soilplot {}>'.format(self.plotname)	

class Soilindicator(db.Model):	
	id=db.Column(db.Integer,primary_key=True)
	indicatorname=db.Column(db.String(50),index=True,unique=True)
	symbol=db.Column(db.String(50))
	unit=db.Column(db.String(50))
	indicatortype=db.Column(db.String(50))
	dland_standard=db.Column(db.Float)
	aland_standard_ph1=db.Column(db.Float)
	aland_standard_ph2=db.Column(db.Float)
	aland_standard_ph3=db.Column(db.Float)
	aland_standard_ph4=db.Column(db.Float)
	soildatas=db.relationship('Soildata',backref='indicator',lazy='dynamic')
	soilshps=db.relationship('Soilshp',backref='indicator',lazy='dynamic')

	def __repr__(self):
		return '<Soilindicator {}>'.format(self.indicatorname)

class Soildata(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	timestamp=db.Column(db.DateTime, default=datetime.utcnow)
	year=db.Column(db.Integer)
	value=db.Column(db.Float)
	indicator_id=db.Column(db.Integer, db.ForeignKey('soilindicator.id'))
	soilplot_id=db.Column(db.Integer, db.ForeignKey('soilplot.id'))

class Soilshp(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	year=db.Column(db.Integer)
	region=db.Column(db.String(50))
	shpurl=db.Column(db.String(586))
	indicator_id=db.Column(db.Integer,db.ForeignKey('soilindicator.id'))

class Societyclass(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	classname=db.Column(db.String(50))
	societyindicators=db.relationship('Societyindicator',backref='societyclass',lazy='dynamic')

class Societyindicator(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	indicatorname=db.Column(db.String(50))
	unit=db.Column(db.String(50))
	class_id=db.Column(db.Integer,db.ForeignKey('societyclass.id'))
	societydatas=db.relationship('Societydata',backref='indicator',lazy='dynamic')

class Societydata(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	timestamp=db.Column(db.DateTime, default=datetime.utcnow)
	value=db.Column(db.Float)
	year=db.Column(db.Integer)
	indicator_id=db.Column(db.Integer, db.ForeignKey('societyindicator.id'))	
