import random
import menu_scraper
from datetime import date
from datetime import time

NUM_SWAPS = 20


def generate_meals(menu_items, cal_target, dv_alloc, low_carb, low_fat, low_sugar):
    random.seed(time.microsecond)
    curr_menu = sorted(menu_items, key=lambda d: d['calories'], reverse=True)
    excluded = []
    curr_cals = 0
    for i in menu_items:
        curr_cals = curr_cals + i['calories']

    while curr_cals > cal_target + 100:
        item = curr_menu.pop()
        excluded.insert(0, item)
        curr_cals = curr_cals - item['calories']

    if len(excluded) == 0:
        return curr_menu

    i = NUM_SWAPS
    while i > 0:
        i = i - 1
        out_ind = random.randint(0, len(curr_menu))
        while True:
            in_ind = random.randint(0, len(excluded))
            swap = False
            if low_carb:
                if curr_menu[out_ind]['carbs'] > excluded[in_ind]['carbs']:
                    swap = True
            if low_sugar and not swap:
                if curr_menu[out_ind]['sugar'] > excluded[in_ind]['sugar']:
                    swap = True
            if low_fat and not swap:
                if curr_menu[out_ind]['fat'] > excluded[in_ind]['fat'] or \
                    curr_menu[out_ind]['sat_fat'] > excluded[in_ind]['sat_fat'] or \
                        curr_menu[out_ind]['trans_fat'] > excluded[in_ind]['trans_fat']:
                    swap = True
            out = curr_menu[out_ind]
            curr_menu[out_ind] = excluded[in_ind]
            excluded[in_ind] = out
            if curr_cals > cal_target - 50:
                break
            else:
                while curr_cals < cal_target - 100 or curr_cals > cal_target + 100:
                    if curr_cals < cal_target - 100:
                        in_ind = random.randint(0, len(excluded))
                        item = excluded.pop(in_ind)
                        curr_cals = curr_cals + item['calories']
                        curr_menu.append(item)
                    else:
                        out_ind = random.randint(0, len(curr_menu))
                        item = curr_menu.pop(out_ind)
                        curr_cals = curr_cals - item['calories']
                        excluded.append(item)

    return curr_menu


if __name__ == '__main__':
    vals = menu_scraper.get_day_menu(date.today())
    print(generate_meals(vals[0:30], 600, 22, True, False, False))
    print(generate_meals(vals[0:30], 600, 22, True, False, False))
    print(generate_meals(vals[0:30], 600, 22, True, False, False))
    print(generate_meals(vals[0:30], 600, 22, True, False, False))
