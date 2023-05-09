import io
import csv

from django.core.mail import EmailMessage
from recipes.constants import default_email
from recipes.models import Recipe, Instructions
from ingredients.models import Ingredients, IngredientRecipeMapping


class DataExtraction:

    def extract_data(self, recipes, ingredients, details, quantity_df, quantity_unit_df, recipient):
        print("Starting extraction and structuring of collected data...")
        recipes_ingredients, recipe_details, duplicate_values = self.structure_all_data(recipes, ingredients, details, quantity_df, quantity_unit_df)

        print("Starting database insertion...")
        errors, successful_count, failed_count = self.insert_data_to_db(recipe_details, recipes_ingredients)

        print("Database insertion completed. Sending email...")
        DataExtractionReport().send_data_report(recipient, errors, successful_count, failed_count)


    def insert_data_to_db(self, recipe_details, recipes_ingredients):
        errors = {}
        successful_count = 0
        failed_count = 0
        for k,v in recipe_details.items():
            try:
                recipe = Recipe.objects.create(
                    name = k,
                    recipe_type = v["recipe_type"],
                    alternate_name = v["alternate_name"],
                    description = v["description"],
                    meat_type = v["meat_type"],
                    meat_classfication = v["meat_classification"],
                    cuisine = v["cuisine"],
                    serving_quantity = v["serving_quantity"],
                    serves = v["serve"],
                    meal_type = v["meal_type"],
                    cookwares = v["cookware"],
                )
                recipe.save()
                recipe_instructions = Instructions.objects.create(
                    recipe = recipe,
                    pre_cooking_steps = v["pre_cooking"],
                    cooking_steps = v["cooking"],
                    tips = v["tips"],
                    total_duration = v["time"]
                )
                recipe_instructions.save()
                for i in recipes_ingredients[k]:
                    item, _ = Ingredients.objects.get_or_create(name=i["Actual"])
                    recipeIngredient = IngredientRecipeMapping.objects.create(
                        recipe = recipe,
                        ingredient = item,
                        comments = i["comments"],
                        quantity = i["quantity"],
                        measuring_unit = i["quantity_unit"],
                        alternate_ingredient = i["Alternate"]
                    )
                    recipeIngredient.save()
                successful_count += 1
            except Exception as e:
                errors[k] = {"error": e, "start_index": v["start_row"], "end_index": v["end_row"]}
                failed_count += 1
                continue

        return errors, successful_count, failed_count

    def structure_all_data(self, recipes, ingredients, details, quantity_df, quantity_unit_df):
        recipes_ingredients = {}
        recipe_details = {}
        duplicate_values = []
        counter = 1
        indices = recipes.index

        for i in recipes.itertuples():
            if i.Recipe_Name not in recipes_ingredients.keys():
                recipes_ingredients[i.Recipe_Name]=[]
                recipe_details[i.Recipe_Name] = {}
            else:
                duplicate_values.append(i)
                continue

            ingredient_list = ingredients.iloc[(i[0]):(indices[counter]),:]

            recipe_details[i.Recipe_Name]["start_row"] = i[0]
            recipe_details[i.Recipe_Name]["end_row"] = indices[counter]

            recipe_details[i.Recipe_Name]["alternate_name"] = i.Alternate_Name
            recipe_details[i.Recipe_Name]["recipe_type"] = i.Recipe_Type
            recipe_details[i.Recipe_Name]["description"] = i.Description
            recipe_details[i.Recipe_Name]["meat_type"] = i.Meat_Type
            recipe_details[i.Recipe_Name]["meat_classification"] = i.Meat_Classification
            recipe_details[i.Recipe_Name]["cuisine"] = i.Cuisine
            recipe_details[i.Recipe_Name]["serving_quantity"] = i.Serving_Quantity
            recipe_details[i.Recipe_Name]["serve"] = i.Serve
            recipe_details[i.Recipe_Name]["meal_type"] = i.meal_type
            recipe_details[i.Recipe_Name]["cookware"] = i.Cookware
            recipe_details[i.Recipe_Name]["pre_cooking"] = details.iloc[counter]["Pre-Cooking"]
            recipe_details[i.Recipe_Name]["cooking"] = details.iloc[counter]["Cooking"]
            details.iloc[counter].fillna("")
            recipe_details[i.Recipe_Name]["tips"] = {
                "cook_tip":details.iloc[counter]["CookTip"],
                "serve_tip":details.iloc[counter]["ServeTip"],
                "other":details.iloc[counter]["Others"]
            }
            recipe_details[i.Recipe_Name]["time"] = details.iloc[counter]["Total_time"]

            for j in ingredient_list.itertuples():
                    ingredient_details = {}
                    try:
                        ingredient_details = {
                            "Actual":j.Actual, 
                            "Alternate":j.Alternate,
                            "comments":j.Comments,
                            "quantity": quantity_df.iloc[j[0]][quantity_unit_df.iloc[j[0]]],
                            "quantity_unit": quantity_unit_df.iloc[j[0]]
                        }
                    except KeyError:
                        ingredient_details = {
                            "Actual":j.Actual, 
                            "Alternate":j.Alternate,
                            "comments":j.Comments,
                            "quantity": None,
                            "quantity_unit": None
                        }
                    recipes_ingredients[i.Recipe_Name].append(ingredient_details)
            counter += 1

        return recipes_ingredients, recipe_details, duplicate_values
    

class DataExtractionReport:

    def send_report(self):
        pass

    def generate_failure_csv(self, errors):
        output_file = io.StringIO()
        csv_writer = csv.DictWriter(output_file, delimiter=',', fieldnames=["Recipe", "Start Row", "End Row", "Error"])
        csv_writer.writeheader()
        for k,v in errors.items():
            data = {}
            data["Recipe"] = k
            data["Start Row"] = v["start_index"] + 2
            data["End Row"] = v["end_index"] + 1
            data["Error"] = v["error"]
            csv_writer.writerow(data)
        output_file.seek(0)
        return output_file


    def send_data_report(self, recipient, errors, successful_count, failed_count):
        print(recipient)
        message = "The excel file data import stats are as follows: \n\n Successful DB records created - {0}".format(successful_count)
        message += "\n Failed record creation - {0}. \n Find details of failed recipes in attached file.".format(failed_count)
        email = EmailMessage(
            "Greetings,",
            message,
            "youremail@signupaddress.com",
            [recipient]
        )
        if failed_count:
            csv_file = self.generate_failure_csv(errors)
            email.attach("failed_record_info.csv", csv_file.read())

        email.send(fail_silently=False)