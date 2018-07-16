from flask import Blueprint

bp=Blueprint('air',__name__)

from app.air import routes
