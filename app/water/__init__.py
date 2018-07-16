from flask import Blueprint

bp=Blueprint('water',__name__)

from app.water import routes
