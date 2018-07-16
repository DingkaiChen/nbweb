from flask import Blueprint

bp=Blueprint('soil',__name__)

from app.soil import routes
