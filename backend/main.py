import menu
import db
from server import app
from json import dumps
from flask import request
from datetime import date

@app.route('/api/get-meal-plan')
@db.needs_db('session')
def get_meal_plan(session):
    low_carbon = request.args.get('lowcarbon')
    low_sugar = request.args.get('lowsugar')
    low_carbs = request.args.get('lowcarbs')
    low_fat = request.args.get('lowfat')
    req_date = request.args.get('date')

    if req_date is None:
        req_date = str(date.today())

    items = session.query(menu.MenuItem).filter(menu.MenuItem.date == req_date).all()
    return dumps([row.simplified() for row in items])

