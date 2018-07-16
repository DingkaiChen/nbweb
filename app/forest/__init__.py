from flask import Blueprint

bp=Blueprint('forest',__name__)

from app.forest import routes
