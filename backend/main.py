import menu
import db
from server import app
from json import dumps
from flask import request

@app.route('/api/get-meal-plan')
def get_meal_plan():
    low_carbon = request.args.get('lowcarbon')
    low_sugar = request.args.get('lowsugar')
    low_carbs = request.args.get('lowcarbs')
    low_fat = request.args.get('lowfat')
    img = 'https://menu.dining.ucla.edu/Content/Images/RecipeImages/165152.jpg'
    return f'<pre>carbon: {low_carbon}\nsugar: {low_sugar}\ncarbs: {low_carbs}\nfat: {low_fat}</pre></br><img src={img}></img>'

@app.route('/temptest')
@db.needs_db('sess')
def choose(sess):
    beef = menu.MenuItem(name='beef')
    sess.add_all([beef])
    statement = db.select(menu.MenuItem)
    result = sess.scalars(statement).all()
    return dumps([row.simplified() for row in result])
