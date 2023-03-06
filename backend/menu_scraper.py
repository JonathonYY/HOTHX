import requests
import re
from datetime import date
import db
import menu


def get_day_menu(menu_date):
    base_url = 'https://menu.dining.ucla.edu/Menus/' + str(menu_date)
    breakfast = requests.get(base_url + "/Breakfast")
    lunch = requests.get(base_url + "/Lunch")
    dinner = requests.get(base_url + "/Dinner")
    vals = parse_meal(breakfast.text, "Breakfast") + parse_meal(lunch.text, "Lunch") + parse_meal(dinner.text, "Dinner")
    return vals


def parse_meal(source, meal):
    # parse portion of daily menu, for a specific meal
    epic = None
    de_neve = None
    b_plate = None
    if meal == 'Dinner':
        text = source.split('<h3 class="col-header">Epicuria</h3>')[1]
        epic, text = text.split('<h3 class="col-header">De Neve</h3>')
        de_neve, b_plate = text.split('<h3 class="col-header">Bruin Plate</h3>')
    else:
        text = source.split('<h3 class="col-header">De Neve</h3>')[1]
        de_neve, b_plate = text.split('<h3 class="col-header">Bruin Plate</h3>')

    vals = []

    menu_link = r'https://menu.dining.ucla.edu/Recipes/[0-9]*/[0-9!]*'
    if epic:
        matches = re.findall(menu_link, epic)
        for match in matches:
            v = parse_recipe(match, 'Epicuria', meal)
            if v:
                vals.append(v)

    if de_neve:
        matches = re.findall(menu_link, de_neve)
        for match in matches:
            v = parse_recipe(match, 'De Neve', meal)
            if v:
                vals.append(v)

    if b_plate:
        matches = re.findall(menu_link, b_plate)
        for match in matches:
            v = parse_recipe(match, 'Bruin Plate', meal)
            if v:
                vals.append(v)

    return vals


def parse_recipe(url, hall, time):
    r = requests.get(url)
    vals = {'meal': time, 'hall': hall, 'carbon_score': 0, 'name': '', 'calories': 0,
            'fat': 0, 'sat_fat': 0, 'chol': 0, 'sodium': 0, 'carbs': 0, 'protein': 0,
            'calcium_dv': 0, 'iron_dv': 0, 'potassium_dv': 0, 'vit_d_dv': 0, 'fat_dv': 0,
            'sat_fat_dv': 0, 'chol_dv': 0, 'sodium_dv': 0, 'carbs_dv': 0, 'fiber': 0,
            'fiber_dv': 0, 'sugar': 0, 'im_url': '', 'trans_fat': 0, 'vegetarian': 0,
            'vegan': 0, 'peanuts': 0, 'tree_nuts': 0, 'wheat': 0, 'gluten': 0, 'soy': 0,
            'sesame': 0, 'dairy': 0, 'eggs': 0, 'shellfish': 0, 'fish': 0, 'halal': 0}

    # Extract name
    pattern = '<title>(.*)</title>'
    m = re.search(pattern, r.text)
    if m:
        if m.group(1) == 'UCLA Dining Services':
            return
        vals['name'] = m.group(1).replace('&amp;', '&').replace('&#233;', 'e').replace('&#39;',
                                                                                       "'").replace('&#225;', 'a')
    # Extract carbon score
    if 'Low Carbon Footprint' in r.text:
        vals['carbon_score'] = 1
    elif 'High Carbon Footprint' in r.text:
        vals['carbon_score'] = -1

    # Check Dietary Restrictions
    if 'Vegan Menu Option' in r.text:
        vals['vegan'] = 1
        vals['vegetarian'] = 1
    elif 'Vegetarian Menu Option' in r.text:
        vals['vegetarian'] = 1
    if 'Contains Peanuts' in r.text:
        vals['peanuts'] = 1
    if 'Contains Tree Nuts' in r.text:
        vals['tree_nuts'] = 1
    if 'Contains Wheat' in r.text:
        vals['wheat'] = 1
    if 'Contains Gluten' in r.text:
        vals['gluten'] = 1
    if 'Contains Soy' in r.text:
        vals['soy'] = 1
    if 'Contains Sesame' in r.text:
        vals['sesame'] = 1
    if 'Contains Dairy' in r.text:
        vals['dairy'] = 1
    if 'Contains Eggs' in r.text:
        vals['eggs'] = 1
    if 'Contains Crustacean Shellfish' in r.text:
        vals['shellfish'] = 1
    if 'Contains Fish' in r.text:
        vals['fish'] = 1
    if 'Halal Menu Option' in r.text:
        vals['halal'] = 1

    # Extract image source
    pattern = '/Content/Images/RecipeImages/[0-9]*.jpg'
    m = re.search(pattern, r.text)
    if m:
        vals['im_url'] = 'https://menu.dining.ucla.edu/' + m.group(0)

    text = r.text.split('nfbox')[1]
    text = text.split('Percent Daily Values')[0]

    # Extract calories
    pattern = 'Calories[^0-9]*([0-9]+)'
    m = re.search(pattern, text)
    if m:
        vals['calories'] = m.group(1)

    # Extract fat
    pattern = 'Total Fat[^0-9]*([0-9.]+)g[^0-9]*([0-9.]+)'
    m = re.search(pattern, text)
    if m:
        vals['fat'] = m.group(1)
        vals['fat_dv'] = m.group(2)

    pattern = 'Saturated Fat[^0-9]*([0-9.]+)g[^0-9]*([0-9.]+)'
    m = re.search(pattern, text)
    if m:
        vals['sat_fat'] = m.group(1)
        vals['sat_fat_dv'] = m.group(2)

    pattern = 'Trans Fat[^0-9]*([0-9.]+)g'
    m = re.search(pattern, text)
    if m:
        vals['trans_fat'] = m.group(1)

    # Extract cholesterol
    pattern = 'Cholesterol[^0-9]*([0-9.]+)mg[^0-9]*([0-9.]+)'
    m = re.search(pattern, text)
    if m:
        vals['chol'] = m.group(1)
        vals['chol_dv'] = m.group(2)

    # Extract sodium
    pattern = 'Sodium[^0-9]*([0-9.]+)mg[^0-9]*([0-9.]+)'
    m = re.search(pattern, text)
    if m:
        vals['sodium'] = m.group(1)
        vals['sodium_dv'] = m.group(2)

    # Extract carbs
    pattern = 'Total Carbohydrate[^0-9]*([0-9.]+)g[^0-9]*([0-9.]+)'
    m = re.search(pattern, text)
    if m:
        vals['carbs'] = m.group(1)
        vals['carbs_dv'] = m.group(2)

    # Extract fiber
    pattern = 'Dietary Fiber[^0-9]*([0-9.]+)g[^0-9]*([0-9.]+)'
    m = re.search(pattern, text)
    if m:
        vals['fiber'] = m.group(1)
        vals['fiber_dv'] = m.group(2)

    # Extract sugar
    pattern = 'Sugars[^0-9]*([0-9.]+)g'
    m = re.search(pattern, text)
    if m:
        vals['sugar'] = m.group(1)

    # Extract protein
    pattern = 'Protein[^0-9]*([0-9.]+)g'
    m = re.search(pattern, text)
    if m:
        vals['protein'] = m.group(1)

    # Extract Calcium/Iron/Potassium/Vitamin D
    text = text.split('Calcium')[1]
    calcium, text = text.split('Iron')
    iron, text = text.split('Potassium')
    potassium, vitamin_d = text.split('Vitamin D')
    pattern = '([0-9.]+)%'
    m = re.search(pattern, calcium)
    if m:
        vals['calcium_dv'] = m.group(1)
    m = re.search(pattern, iron)
    if m:
        vals['iron_dv'] = m.group(1)
    m = re.search(pattern, potassium)
    if m:
        vals['potassium_dv'] = m.group(1)
    m = re.search(pattern, vitamin_d)
    if m:
        vals['vit_d_dv'] = m.group(1)

    return vals


@db.needs_db('sess')
def upload_meals(sess):
    items = map(menu.MenuItem, get_day_menu(date.today()))
    sess.add_all(items)


if __name__ == '__main__':
    # vals = get_day_menu(date.today())
    # for recipe in vals:
    #     print(recipe)
    # print(len(vals))
    upload_meals()
