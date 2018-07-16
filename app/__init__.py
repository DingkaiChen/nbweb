from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail

db=SQLAlchemy()
migrate=Migrate()
login=LoginManager()
login.login_view='auth.login'
login.login_message='请先登录系统'
bootstrap=Bootstrap()
mail=Mail()

def create_app(config_class=Config):
	app=Flask(__name__)
	app.config.from_object(config_class)

	db.init_app(app)
	migrate.init_app(app,db)
	login.init_app(app)
	bootstrap.init_app(app)
	mail.init_app(app)

	#blueprint registration
	from app.auth import bp as auth_bp
	app.register_blueprint(auth_bp, url_prefix='/auth')

	from app.main import bp as main_bp
	app.register_blueprint(main_bp)
	
	from app.air import bp as air_bp
	app.register_blueprint(air_bp)

	from app.water import bp as water_bp
	app.register_blueprint(water_bp)

	from app.soil import bp as soil_bp
	app.register_blueprint(soil_bp)
	
	from app.forest import bp as forest_bp
	app.register_blueprint(forest_bp)

	from app.map import bp as map_bp
	app.register_blueprint(map_bp)
		
	return app

from app import models
