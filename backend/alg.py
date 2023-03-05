import random
import menu_scraper
from datetime import date
import time

NUM_SWAPS = 5


def generate_meals(menu_items, cal_target, dv_alloc, low_carb, low_fat, low_sugar):
    random.seed(time.time_ns())
    curr_menu = sorted(menu_items, key=lambda d: d['calories'], reverse=True)
    excluded = []
    curr_cals = 0
    for i in menu_items:
        curr_cals = curr_cals + i['calories']

    while curr_cals > cal_target + 200:
        item = curr_menu.pop()
        excluded.insert(0, item)
        curr_cals = curr_cals - item['calories']

    if len(excluded) == 0:
        return curr_menu

    i = NUM_SWAPS
    while i > 0:
        i = i - 1
        out_ind = random.randint(0, len(curr_menu) - 1)
        out_item = curr_menu.pop(out_ind)
        curr_cals = curr_cals - out_item['calories']
        excluded = sorted(excluded, key=lambda d: d['calories'], reverse=False)
        while curr_cals < cal_target - 200:
            in_item = excluded.pop()
            curr_cals = curr_cals + in_item['calories']
            curr_menu.append(in_item)

    curr_menu = sorted(curr_menu, key=lambda d: d['calories'], reverse=True)
    while curr_cals > cal_target + 200:
        item = curr_menu.pop()
        excluded.insert(0, item)
        curr_cals = curr_cals - item['calories']
    return curr_menu


if __name__ == '__main__':
    vals = menu_scraper.get_day_menu(date.today())
    print(generate_meals(vals, 600, 22, True, False, False))
    print(generate_meals(vals, 600, 22, True, False, False))
    print(generate_meals(vals, 600, 22, True, False, False))
    print(generate_meals(vals, 600, 22, True, False, False))
