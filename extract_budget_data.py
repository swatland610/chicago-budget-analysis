import pandas as pd
import requests
import json

# extract budget datas
class Extract:
    def __init__(self):
        self.extract_budgets = Extract.portal_data()

    # creating a class to store the budget year with api endpoint
    class Budget_Data:
        def __init__(self, budget_year, endpoint_id):
            self.budget_year = budget_year
            self.endpoint_id = endpoint_id 

    def build_budget_objects():
        # Create Budget Objects with Budget Year and endpoint id
        budgets_list = [
            Extract.Budget_Data(2011, 'drv3-jzqp'),
            Extract.Budget_Data(2012, '8ix6-nb7q'),
            Extract.Budget_Data(2013, 'b24i-nwag'),
            Extract.Budget_Data(2014, 'ub6s-xy6e'),
            Extract.Budget_Data(2015, 'qnek-cfpp'),
            Extract.Budget_Data(2016, '36y7-5nnf'),
            Extract.Budget_Data(2017, '7jem-9wyw'),
            Extract.Budget_Data(2018, '6g7p-xnsy'),
            Extract.Budget_Data(2019, 'h9rt-tsn7'),
            Extract.Budget_Data(2020, 'fyin-2vyd'),
            Extract.Budget_Data(2021, '6tbx-h7y2')
        ]
        return budgets_list  
    
    def portal_data():
        # Bring in Budgets
        budgets_list = Extract.build_budget_objects()

        # initiate Empty Dataframe Object to use concat 
        ## in the budget datasets, columns are at the same index, but occasionaly have different labels
        ## assigning index values for columns for easier matching later on
        ten_year_budgets = pd.DataFrame(columns=[int(i) for i in range(0,11)])

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

            # add a check to see if budget year = 2011 as there is an extra column we do not need in this data set
            if budget_year == 2011:
                budget_data.drop(columns='department', inplace=True)
            # if it is not 2011, then we just move on    
            else:
                pass

            # convert column names to index values so we can easier concat dataframes
            budget_data.rename(columns={x:y for x,y in zip(budget_data.columns, range(0,len(budget_data.columns)))},
                               inplace=True)

            # Stack these Budget DataFrames on top of one another
            ten_year_budgets = pd.concat([ten_year_budgets, budget_data], ignore_index=True)

        return ten_year_budgets

    def pull_department_names():
        # In our larger dataset
        url = 'https://data.cityofchicago.org/resource/{}.json' 