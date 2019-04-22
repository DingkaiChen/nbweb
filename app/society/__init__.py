from flask import Blueprint

bp=Blueprint('society',__name__)

from app.society import routes
