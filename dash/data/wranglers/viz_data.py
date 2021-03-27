import pandas as pd
import json 

class Data_Viz_Data:
    def __init__(self):
        # just pull all ten years as a Dataframe
        self.ten_year_budgets = pd.read_csv('data/ten_year_budgets.csv', index_col="Unnamed: 0")

    # total budget for each year
    def get_annual_budget_totals(self):
        data = Data_Viz_Data().ten_year_budgets 
        annual_budgets_totals = data.groupby('budget_year').agg({'amount':'sum'})
        return annual_budgets_totals
    