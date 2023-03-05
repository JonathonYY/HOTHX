import menu
import db
from server import app
from json import dumps
from flask import request
from datetime import date
from random import randrange
from alg import generate_meals

@db.needs_db('session')
def get_with_restrictions(filter_clause, meal, hall, session):
    filter = filter_clause[:]
    filter.append(menu.MenuItem.hall == hall)
    filter.append(menu.MenuItem.meal == meal)
    result = session.query(menu.MenuItem).filter(*filter).all()
    return [row.simplified() for row in result]

@app.route('/api/get-meal-plan')
def get_meal_plan():
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

    breakfasts = [get_with_restrictions(filter_clause, 'Breakfast', 'De Neve'),
                  get_with_restrictions(filter_clause, 'Breakfast', 'Bruin Plate')]
    lunches = [get_with_restrictions(filter_clause, 'Lunch', 'De Neve'),
             get_with_restrictions(filter_clause, 'Lunch', 'Bruin Plate')]
    dinners = [get_with_restrictions(filter_clause, 'Dinner', 'De Neve'),
              get_with_restrictions(filter_clause, 'Dinner', 'Bruin Plate'),
              get_with_restrictions(filter_clause, 'Dinner', 'Epicuria')]

    breakfast = breakfasts[randrange(0, len(breakfasts))]
    lunch = lunches[randrange(0, len(lunches))]
    dinner = dinners[randrange(0, len(dinners))]

    return dumps({
        'breakfast': generate_meals(breakfasts[0], 600, True, True, False, False),
        'lunch': generate_meals(lunches[1], 600, False, False, False, True),
        'dinner': generate_meals(dinners[2], 800, True, True, False, True)
    })
