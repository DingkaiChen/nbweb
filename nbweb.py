from app import create_app,db
from app.models import Role,Register,User,Post,Airplot,Voctype,Airdata,Vocdata,Forestplot,Arbor,Arbortype,Arborsample,Herbquadrat,Herbsample,Herbtype,Herb,Soildata,Soilplot,Soilindicator

app=create_app()

@app.shell_context_processor
def make_shell_context():
	return {'db':db, 'User':User, 'Role':Role, 'Register':Register, 'Post':Post, 'Airplot':Airplot, 'Voctype':Voctype, 'Airdata':Airdata, 'Vocdata':Vocdata, 'Forestplot':Forestplot, 'Arbor':Arbor, 'Herbquadrat':Herbquadrat, 'Herbsample':Herbsample, 'Herbtype':Herbtype, 'Herb':Herb, 'Arbortype':Arbortype, 'Arborsample':Arborsample, 'Soilplot':Soilplot, 'Soilindicator':Soilindicator, 'Soildata':'Soildata'}
