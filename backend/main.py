import menu
import db
from server import app
from json import dumps
from flask import request
from datetime import date

@app.route('/api/get-meal-plan')
@db.needs_db('session')
def get_meal_plan(session):
    flags = ['vegetarian', 'vegan', 'peanut', 'eggs', 'treenut', 'wheat', 'gluten', 'soy', 'sesame',
             'dairy', 'shellfish', 'fish', 'halal', 'lowcarbon', 'lowsugar', 'lowcarbs', 'lowfat']
    menu_flag = [menu.MenuItem.vegetarian, menu.MenuItem.vegan, menu.MenuItem.peanuts, menu.MenuItem.eggs,
                 menu.MenuItem.tree_nuts, menu.MenuItem.wheat, menu.MenuItem.gluten, menu.MenuItem.soy,
                 menu.MenuItem.sesame, menu.MenuItem.dairy, menu.MenuItem.shellfish, menu.MenuItem.fish,
                 menu.MenuItem.halal]
    req_date = request.args.get('date') or str(date.today())

    filter_clause = [menu.MenuItem.date == req_date]
    for (index, flag) in enumerate(flags):
        req = request.args.get(flag)
        if req is not None:
            filter_clause.append(menu_flag[index] == int(req))

    items = session.query(menu.MenuItem).filter(*filter_clause).all()

    return dumps([row.simplified() for row in items])
