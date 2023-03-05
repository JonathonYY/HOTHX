import requests
import re
from datetime import date


def get_day_menu(menu_date):
    url = 'https://menu.dining.ucla.edu/Menus/' + str(menu_date)
    r = requests.get(url)
    text = r.text.split('Breakfast Menu for Today, ')[1]
    breakfast, text = text.split('Lunch Menu for Today, ')
    lunch, dinner = text.split('Dinner Menu for Today, ')
    parse_meal(breakfast, "Breakfast")
    parse_meal(lunch, "Lunch")
    parse_meal(dinner, "Dinner")


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

    menu_link = r'https://menu.dining.ucla.edu/Recipes/[0-9]*/[0-9!]*'
    if epic:
        matches = re.findall(menu_link, epic)
        for match in matches:
            parse_recipe(match, 'Epicuria', meal)

    if de_neve:
        matches = re.findall(menu_link, de_neve)
        for match in matches:
            parse_recipe(match, 'De Neve', meal)

    if b_plate:
        matches = re.findall(menu_link, b_plate)
        for match in matches:
            parse_recipe(match, 'Bruin Plate', meal)


def parse_recipe(url, hall, time):
    r = requests.get(url)
    vals = {'meal': time, 'hall': hall, 'carbon_score': 0, 'name': None, 'calories': None,
            'fat': None, 'sat_fat': None, 'chol': None, 'sodium': None, 'carbs': None,
            'protein': None, 'calcium_dv': None, 'iron_dv': None, 'potassium_dv': None,
            'vit_d_dv': None, 'fat_dv': None, 'sat_fat_dv': None, 'chol_dv': None,
            'sodium_dv': None, 'carbs_dv': None, 'fiber': None, 'fiber_dv': None,
            'sugar': None, 'im_url': None, 'trans_fat': None}

    # Extract name
    pattern = '<title>(.*)</title>'
    m = re.search(pattern, r.text)
    if m:
        if m.group(1) == 'UCLA Dining Services':
            return
        vals['name'] = m.group(1).replace('&amp;', '&')

    # Extract carbon score
    if 'Low Carbon Footprint' in r.text:
        vals['carbon_score'] = 1
    elif 'High Carbon Footprint' in r.text:
        vals['carbon_score'] = -1

    # Extract image source
    pattern = '/Content/Images/RecipeImages/[0-9]*.jpg'
    m = re.search(pattern, r.text)
    if m:
        vals['im_url'] = 'https://menu.dining.ucla.edu/' + m.group(0)

    text = r.text.split('nfbox')[1]
    text = text.split('Percent Daily Values')[0]

    # Extract calories
    pattern = 'Calories[^0-9]*([0-9]*)'
    m = re.search(pattern, text)
    if m:
        vals['calories'] = m.group(1)

    # Extract fat
    pattern = 'Total Fat[^0-9]*([0-9.]*)g[^0-9]*([0-9.]*)'
    m = re.search(pattern, text)
    if m:
        vals['fat'] = m.group(1)
        vals['fat_dv'] = m.group(2)

    pattern = 'Saturated Fat[^0-9]*([0-9.]*)g[^0-9]*([0-9.]*)'
    m = re.search(pattern, text)
    if m:
        vals['sat_fat'] = m.group(1)
        vals['sat_fat_dv'] = m.group(2)

    pattern = 'Trans Fat[^0-9]*([0-9.]*)g'
    m = re.search(pattern, text)
    if m:
        vals['trans_fat'] = m.group(1)

    # Extract cholesterol
    pattern = 'Cholesterol[^0-9]*([0-9.]*)mg[^0-9]*([0-9.]*)'
    m = re.search(pattern, text)
    if m:
        vals['chol'] = m.group(1)
        vals['chol_dv'] = m.group(2)

    # Extract sodium
    pattern = 'Sodium[^0-9]*([0-9.]*)mg[^0-9]*([0-9.]*)'
    m = re.search(pattern, text)
    if m:
        vals['sodium'] = m.group(1)
        vals['sodium_dv'] = m.group(2)

    # Extract carbs
    pattern = 'Total Carbohydrate[^0-9]*([0-9.]*)g[^0-9]*([0-9.]*)'
    m = re.search(pattern, text)
    if m:
        vals['carbs'] = m.group(1)
        vals['carbs_dv'] = m.group(2)

    # Extract fiber
    pattern = 'Dietary Fiber[^0-9]*([0-9.]*)g[^0-9]*([0-9.]*)'
    m = re.search(pattern, text)
    if m:
        vals['fiber'] = m.group(1)
        vals['fiber_dv'] = m.group(2)

    # Extract sugar
    pattern = 'Sugars[^0-9]*([0-9.]*)g'
    m = re.search(pattern, text)
    if m:
        vals['sugar'] = m.group(1)

    # Extract protein
    pattern = 'Protein[^0-9]*([0-9.]*)g'
    m = re.search(pattern, text)
    if m:
        vals['protein'] = m.group(1)

    # Extract Calcium/Iron/Potassium/Vitamin D
    text = text.split('Calcium')[1]
    calcium, text = text.split('Iron')
    iron, text = text.split('Potassium')
    potassium, vitamin_d = text.split('Vitamin D')
    pattern = '([0-9.]*)%'
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

    print(vals)


if __name__ == '__main__':
    get_day_menu(date.today())
