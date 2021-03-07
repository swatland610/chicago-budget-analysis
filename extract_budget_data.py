import pandas as pd
import requests
import json

# extract budget datas
class Extract_Budget_Data:
    def __init__(self):
        extract_portal_data()
    
    def extract_portal_data():
        # Bring in Budgets
        budgets_list = build_budget_objects()

        # initiate Empty Dataframe Object to use concat 
        ## in the budget datasets, columns are at the same index, but occasionaly have different labels
        ## assigning index values for columns for easier matching later on
        ten_year_budgets = pd.DataFrame(columns=[i for i in range(0,11)])

        # iterate through budget list
        for budget in budgets_list:

            # set budget year and url for pulling api data
            budget_year = budget.budget_year
            url = 'https://data.cityofchicago.org/resource/{}.json'.format(budget.endpoint_id)

            # initiate get request
            response = requests.get(url)
            response_dict = json.loads(response.text)

            # load into DF
            budget_data = pd.DataFrame(response_dict)

            # add a budget year column
            budget_data['budget_year'] = budget_year

            # convert column names to index values so we can easier concat dataframes
            budget_data.rename(columns=lambda col: col.index, inplace=True)

            return budget_data


    # creating a class to store the budget year with api endpoint
    class Budget_Data:
        def __init__(self, budget_year, endpoint_id):
            self.budget_year = budget_year
            self.endpoint_id = endpoint_id

    def build_budget_objects():
        # Create Budget Objects with Budget Year and enpoint id
        bugdets_list = [
            Budget_Data(2011, 'drv3-jzqp'),
            Budget_Data(2012, '8ix6-nb7q'),
            Budget_Data(2013, 'b24i-nwag'),
            Budget_Data(2014, 'ub6s-xy6e'),
            Budget_Data(2015, 'qnek-cfpp'),
            Budget_Data(2016, '36y7-5nnf'),
            Budget_Data(2017, '7jem-9wyw'),
            Budget_Data(2018, '6g7p-xnsy'),
            Budget_Data(2019, 'h9rt-tsn7'),
            Budget_Data(2020, 'fyin-2vyd'),
            Budget_Data(2021, '6tbx-h7y2')
        ]
        return budgets_list        

