import pandas as pd
from recipes.data_extraction_util import DataExtraction


class DataCollection:
    """
        This is a utility class designed to ease the import of recipe data from excel file format.
        This class can be extended for further use with csv and other formats.
    """

    @staticmethod
    def collect_from_excel(filepath, recipient):
        """
            This function is a static method which reads excel file from given filepath 
            and stores it into pandas dataframe followed by starting the extraction of required
            data from the dataframes.
            param: filepath (str)
            return: 
        """
        print("Reading data from excel...")
        df = pd.read_excel(filepath)
        print("Excel data reading completed!")
        DataCollection().collect_data(df, recipient)


    def collect_ingredients_data(self, df):
        """
            This function slices through the dataframe to separate the ingredients
        """
        ingredients = df.iloc[:,14:17]
        ingredients.columns = ingredients.iloc[0]
        quantity_df, quantity_unit_df = self.collect_ingredients_quantity(df)
        return ingredients, quantity_df, quantity_unit_df

    def collect_recipes(self, df):
        """
            This function slices through the dataframe to separate the recipes
        """
        temp_df = df.iloc[:,:14]
        recipes = temp_df.dropna(how='all')
        recipes.columns = recipes.columns.str.replace(" ","_")
        return recipes

    def collect_ingredients_quantity(self, df):
        """
            This function slices through the dataframe to separate the quantity and their measuring units.
        """
        quantity_df = df.iloc[:,17:49]
        quantity_df.columns = quantity_df.iloc[0]
        quantity_unit_df = quantity_df.apply(pd.Series.first_valid_index, axis=1)
        return quantity_df, quantity_unit_df
    
    def collect_recipe_metadata(self, df):
        """
            This function slices through the dataframe to separate the instructions, tips, time, etc
            metadata for the recipes.
        """
        temp_s = df.iloc[:,49:59]
        details = temp_s.dropna(how='all')
        details.columns = details.iloc[0]
        details.columns = details.columns.str.replace(" ","")
        details = details.fillna("")
        return details

    def collect_data(self, df, recipient):
        """
            This function executes step by step execution for collecting data and passes it to extraction class.
        """
        print("Fetching recipes from collected data...")
        recipes = self.collect_recipes(df)

        print("Recipes collected. Collecting ingredients data...")
        ingredients, quantity_df, quantity_unit_df = self.collect_ingredients_data(df)
        
        print("Ingredients and their quantity collected. Collecting other recipe metadata...")
        details = self.collect_recipe_metadata(df)

        print("Metadata collection completed. Starting extraction of data...")
        DataExtraction().extract_data(recipes, ingredients, details, quantity_df, quantity_unit_df, recipient)
        