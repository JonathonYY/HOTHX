import requests
import re

global counter

def get_day_menu():
    r = requests.get('https://menu.dining.ucla.edu/Menus/Today')
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
    if (meal == 'Dinner'):
        text = source.split('<h3 class="col-header">Epicuria</h3>')[1]
        epic, text = text.split('<h3 class="col-header">De Neve</h3>')
        de_neve, b_plate = text.split('<h3 class="col-header">Bruin Plate</h3>')
    else:
        text = source.split('<h3 class="col-header">De Neve</h3>')[1]
        de_neve, b_plate = text.split('<h3 class="col-header">Bruin Plate</h3>')

    menu_link = r'https://menu.dining.ucla.edu/Recipes/[0-9]*/[0-9!]*'
    if epic != None:
        matches = re.findall(menu_link, epic)
        for match in matches:
            parse_recipe(match, 'Epicuria', meal)

    if de_neve != None:
        matches = re.findall(menu_link, de_neve)
        for match in matches:
            parse_recipe(match, 'De Neve', meal)

    if b_plate != None:
        matches = re.findall(menu_link, b_plate)
        for match in matches:
            parse_recipe(match, 'Bruin Plate', meal)

def parse_recipe(url, hall, time):
    # r = requests.get(url)
    # todo
    print(url)

if __name__ == '__main__':
    parse_recipe("https://menu.dining.ucla.edu/Recipes/201025/2", "Bruin Plate", "Dinner")