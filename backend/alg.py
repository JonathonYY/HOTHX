


### DEFINE DEFAULTS FOR EACH PARAMETER HERE

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


# Field names: id, name, calories, fat, sat_fat, chol, sodium, carbs, protein, 
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



    
def determine_score(dict_menu_items, menu_options):

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








def cost_function(dict_menu_items):


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


