


### DEFINE DEFAULTS FOR EACH PARAMETER HERE

CARBON_SCORE_DEFUALT = 15
FAT_DEFAULT = 2
SAT_FAT_DEFAULT = 3
TRANS_FAT_DEFAULT = 6
CHOL_DEFAULT = 6
SODIUM_DEFAULT = 1
CARBS_DEFAULT = 1
FIBER_DEFAULT = 1
SUGAR_DEFAULT = 8
PROTEIN_DEFAULT = 2
PROTEIN_DAILY_AMOUNT = 56 # could add option to change it - recommended formula is 0.8 * body weight (kg)
CALCIUM_DEFUALT = 0.2
IRON_DEFAULT = 0.2
POTASSIUM_DEFAULT = 0.2
VIT_D_DEFAULT = 0.2

DAILY_CALORIE_DEFAULT = 2000

BREAKFAST_PERIOD = 0
LUNCH_PERIOD = 1
DINNER_PERIOD = 2

BREAKFAST_PERCENT = 23
LUNCH_PERCENT = 38.5
DINNER_PERCENT = 38.5

B_PLATE = 0
DE_NEVE = 1
EPICURIA = 2
RENDE = 3
THE_STUDY = 4



# carbon_score: 0 for low carbon, 15 for neutral, 30 for high carbon (double values for low carbon option)
# hall & meal: 0
# calories: 0  # don't really care about the number of calories itself - care more about nutritional value per calorie - > explore how to incorporate that more
# fat: g * 2 until DV reached, after that g * 4 (double for low fat)
# sat_fat: g * 3 until DV reached, after that g * 6 (double for low fat)
# trans_fat: g * 6 (double for low fat)
# chol: mg * 6 until DV reached, after that g * 12
# sodium: mg * 1 until DV reached, after that mg * 2
# carbs: g * 1 until DV reached, after that g * 2 (double for low carbs)
# fiber: ([portion of DV allocated for that meal] - fiber_dv) * 1
# sugar: g * 8 (double for low sugar)
# protein: ( (56 [could change this value per person]* portion of DV allocated to this meal) - protein) * 2
# calcium: ([%dv for this meal] - calcium_dv) * 0.2
# iron ([%dv for this meal] - iron_dv) * 0.2
# potassium: ([%dv for this meal] - potassium_dv) * 0.2
# vitamin d: ([%dv for this meal] - vit_d_dv) * 0.2


# Field names: id, name, calories, fat, sat_fat, trans_fat, chol, sodium, carbs, protein, 
# calcium_dv, iron_dv, potassium_dv, vit_d_dv, fat_dv, sat_fat_dv, chol_dv, 
# sodium_dv, carbs_dv, fiber, fiber_dv, sugar, hall, carbon_score, im_url, meal

# Units:
# Calories: kcal
# Total fat, sat fat, trans fat, total carbs, fiber, sugars, protein: g
# Cholesterol, sodium: mg
# All DVs: %




### END DEFINE DEFUALTS FOR EACH PARAMETER






class menu_item:

def __init__(self, name):
    self.name = name



    
def get_ideal_meal(dict_all_items, dining_hall_choice, dining_hall_period, carbon_flag, carbs_flag, fat_flag, sugar_flag):

    daily_value_portion = 0

    if dining_hall_period == BREAKFAST_PERIOD:
        daily_value_portion = BREAKFAST_PERCENT
    elif dining_hall_period == LUNCH_PERIOD:
        daily_value_portion = LUNCH_PERCENT
    else:
        daily_value_portion = DINNER_PERCENT



    ### GET SCORE FOR EACH MENU ITEM AT THAT DINING HALL ###

    for i in dict_all_items:
        if(i.hall == dining_hall_choice):

            if i.carbon_score == -1: # high carbon
                score += 2 * CARBON_SCORE_DEFUALT
                if carbon_flag == true:
                    score += 2 * CARBON_SCORE_DEFUALT
            elif i.carbon_score == 0:
                i.score += CARBON_SCORE_DEFUALT

        
            if fat_flag == true:
                fat_temp = i.fat if i.fat_dv < daily_value_portion else (i.fat*(daily_value_portion/i.fat_dv))
                fat_remainder = i.fat - fat_temp
                i.score += fat_temp * FAT_DEFAULT * 2
                i.score += fat_remainder * FAT_DEFAULT * 4

                sat_fat_temp = i.sat_fat if i.sat_fat_dv < daily_value_portion else (i.sat_fat*(daily_value_portion/i.sat_fat_dv))
                sat_fat_remainder = i.sat_fat - sat_fat_temp
                i.score += sat_fat_temp * SAT_FAT_DEFAULT * 2
                i.score += sat_fat_remainder * SAT_FAT_DEFAULT * 4

                score += i.trans_fat * TRANS_FAT_DEFAULT * 2
            else:
                fat_temp = i.fat if i.fat_dv < daily_value_portion else (i.fat*(daily_value_portion/i.fat_dv))
                fat_remainder = i.fat - fat_temp
                i.score += fat_temp * FAT_DEFAULT
                i.score += fat_remainder * FAT_DEFAULT * 2

                sat_fat_temp = i.sat_fat if i.sat_fat_dv < daily_value_portion else (i.sat_fat*(daily_value_portion/i.sat_fat_dv))
                sat_fat_remainder = i.sat_fat - sat_fat_temp
                i.score += sat_fat_temp * SAT_FAT_DEFAULT
                i.score += sat_fat_remainder * SAT_FAT_DEFAULT * 2

                i.score += i.trans_fat * TRANS_FAT_DEFAULT


            chol_temp = i.chol if i.chol_dv < daily_value_portion else (i.chol*(daily_value_portion/i.chol_dv))
            chol_remainder = i.chol - chol_temp

            i.score += chol_temp * CHOL_DEFAULT
            i.score += chol_remainder * CHOL_DEFAULT * 2

            sodium_temp = i.sodium if i.sodium_dv < daily_value_portion else (i.sodium*(daily_value_portion/i.sodium_dv))
            sodium_remainder = i.sodium - sodium_temp

            i.score += sodium_temp * CHOL_DEFAULT
            i.score += sodium_remainder * CHOL_DEFAULT * 2

            if carbs_flag == true:
                carbs_temp = i.carbs if i.carbs_dv < daily_value_portion else (i.carbs*(daily_value_portion/i.carbs_dv))
                carbs_remainder = i.carbs - carbs_temp
                i.score += carbs_temp * CARBS_DEFAULT * 2
                i.score += carbs_remainder * CARBS_DEFAULT * 4

            else:
                carbs_temp = i.carbs if i.carbs_dv < daily_value_portion else (i.carbs*(daily_value_portion/i.carbs_dv))
                carbs_remainder = i.carbs - carbs_temp
                i.score += carbs_temp * CARBS_DEFAULT
                i.score += carbs_remainder * CARBS_DEFAULT

            i.score += (daily_value_portion - i.fiber_dv) * FIBER_DEFAULT

            if sugar_flag == true:
                i.score += i.sugar * SUGAR_DEFAULT * 2
            else:
                i.score += i.sugar * SUGAR_DEFAULT

            i.score += ((PROTEIN_DAILY_AMOUNT * daily_value_portion) - i.protein) * PROTEIN_DEFAULT


            i.score += (daily_value_portion - i.calcium_dv) * CALCIUM_DEFUALT
            i.score += (daily_value_portion - i.iron_dv) * IRON_DEFUALT
            i.score += (daily_value_portion - i.potassium_dv) * potassium_DEFUALT
            i.score += (daily_value_portion - i.vit_d_dv) * VIT_D_DEFUALT


    ### SORT ITEMS FROM THAT DINING HALL AND PUT THEM IN A NEW SET ###

    current_menu_items = []

    for i in dict_all_items:
        if(i.hall == dining_hall_choice):
            current_menu_items.add(i)

    current_menu_items.sort(key=lamba x: x.score)


    
         








            





        


















    #note: will do this for each dining hall! then compare the score at each one

    # ideal score: 0
    # for each parameter, 
    # if it is too low (if that's a thing), give a score below 0
    # if it is too high (if that's a thing), give a score above 0
    # total score is sum of (absolute value of score * specified weight for that item)


    # idea: try to approximate DV's for breakfast. Then split remaining DV between lunch & dinner. 
    # Alternatively, could just try to shoot for proportional targets for each meal and ignore excesses/depts from previous meal(s)


    # example:
    # for breakfast:




    # weights will be dependent on menu_options - default values used for each param, 
    # but preferences specified by user can override weight for certain params

    # come up with a score for each item on the menu
    # then sort the menu items based on score
    # determine a potential menu by adding menu items according to the following alg:


    # idea: take a "guess" as to what the best menu combination will be, 
    # then for each item in our guess, iterate through potential replacements of it; if the replacement would lower that whole meal's score, replace it
    # but make sure there is a limit to each individual items so that menu is balanced (maybe 1 or 2 is the default for most menu items)

    # add one of each item until calorie limit (or some other limit) is reached (loop back aroung to begining if you run out of items)
    # once limit is reached, start 'checking' your items 
    # if there is an item that improves overall score without going over that item's limit, replace current item with that item
    # could implement this by adding all possible items to a sorted list - when you replace an item in this menu plan, add it back to the list
    # could do multiple passes of the algorithm
    #
    # 

    # create list of possible items possible_items by adding each item, the number of times determined by [max_amount] 
    # (which can either be a global # like 2 or be determined based on the portion size etc)

        #while (total number of calories < threshold):
            # add front item in possible_items to curr_menu 
            # remove that item from possible_items

        # score_comp = calculate_score(curr_menu)    

        # for i in curr_menu (starting at the end?):
            # for j in possible_items:
                # if calculate_score(curr_menu - i + j) < calculate_score(curr_menu):
                    # remove i 
                    # add j
                    # if total_calories < calorie_threshold: 
                        # add front item of possible_items to curr_menu
                    # if total_calories > calorie_threshold + 400 && [smallest item's calorie count] < 400:
                        # remove lowest-ranked item that will get total below threshold






        
        



            



    # example:








def cost_function(dict_all_items):


    # 0 = BPLATE
    # 1 = DE NEVE
    # 2 = EPICURIA
    # 3 = RENDE
    # 4 = THE STUDY


    breakfast_hall = random.randint(0,4)
    lunch_hall = random.randint(0,4)
    ignore = -1
    if breakfast_hall == lunch_hall:
        ignore = breakfast_hall

    dinner_hall = random.randint(0,4)
    while dinner_hall == ignore:
        dinner_hall = random.randint(0,4)

    ignore = -1


    ### flags ### - *ADD ACTUAL VALUES HERE WHEN U FIND OUT HOW THEY'RE IMPlEMENTED
    carbon_flag = false
    carbs_flag = false
    fat_flag = false
    sugar_flag = false

    


    ideal_breakfast = get_ideal_meal(dict_all_items, breakfast_hall, BREAKFAST_PERIOD, carbon_flag, carbs_flag, fat_flag, sugar_flag)
    ideal_lunch = get_ideal_meal(dict_all_items, lunch_hall, carbon_flag, LUNCH_PERIOD, carbs_flag, fat_flag, sugar_flag)
    ideal_dinner = get_ideal_meal(dict_all_items, dinner_hall, carbon_flag, DINNER_PERIOD, carbs_flag, fat_flag, sugar_flag)
    
        

    

    # choose a random dining hall for breakfast and lunch
    # if the same dining hall was chosen for breakfast and lunch:
    # remove from dinner choices
    # choose a random dining hall for dinner (from pool of dinner choices)

    # for each meal:
    # 

    
    
    # then compare the ideal meal at each dining hall, and determine which one to go to from there (may include user preferences)






def main():
    print("hello world")






























if __name__ == "__main__":
    main()


