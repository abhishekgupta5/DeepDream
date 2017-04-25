# app/home/__init.py

from flask import Blueprint

home = Blueprint('home', __name__)

from . import views

