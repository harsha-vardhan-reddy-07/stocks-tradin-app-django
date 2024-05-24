from django.db import models

from db_connection import db

# Create your models here.

users_collection = db['users']

transactions_collection = db['transactions']

stocks_collection = db['stocks']

orders_collection = db['orders']