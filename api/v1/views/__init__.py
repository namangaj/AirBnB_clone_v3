#!/usr/bin/python3
"""
createw Flask app blueprint.
"""
from api.v1.index import *
from flask import blueprint

app_views = Blueprint('app_views', _name_, url_prefix='/api/vi')
