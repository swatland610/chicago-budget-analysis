import pandas as pd
import requests
import json

# extract budget datas
class Extract:
    def __init__(self):
        self.extract_budgets = Extract.set_col_labels_and_new_department_names()

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
    
    # The next three functions are chained together:
    ## 1. Bring in all 10 sets and concat them on top of each other
    ## 2. Pull 2021 department names to unify naming differences over the years
    ## 3. Rename Columns & Set new values for Department names based on Department ID
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
            # Be sure to make sure the 'limit' is set, as it defaults to only returning 1000 records
            budget_year = budget.budget_year
            url = 'https://data.cityofchicago.org/resource/{}.json?$limit=10000'.format(budget.endpoint_id)

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
        # In our larger dataset the department descriptions vary from year to year, but 
        # the department account id stay the same. Bringing in 2021 Data again to unify the
        # department descriptions so they match 2021's data
        url = 'https://data.cityofchicago.org/resource/6tbx-h7y2.json?$limit=10000' 

        # initiate get request
        response = requests.get(url)
        response_dict = json.loads(response.text)

        # Set DataFrame and Subset to needed Columns
        budget_2021 = pd.DataFrame(response_dict)
        departments_2021 = budget_2021.loc[:][['department_number', 'department_description']].\
                                drop_duplicates(ignore_index=True)

        return departments_2021

    def set_col_labels_and_new_department_names():
        # Bring in two DFs created in the prior 2 functions
        ten_year_budgets = Extract.portal_data()
        departments_2021 = Extract.pull_department_names()

        # first, we are just going to rename the columns
        cols = {0:'fund_type',
                1:'fund_code',
                2:'fund_description',
                3:'department_number',
                4:'department_description',
                5:'approp_authority',
                6:'approp_auth_description',
                7:'approp_account',
                8:'approp_account_description',
                9:'amount',
                10:'budget_year'}

        ten_year_budgets.rename(columns=cols, inplace=True)
        
        # for every id, find matching department id in ten_year_budgets and change the value
        departments_2021_ids = departments_2021['department_number'].to_list()

        for dept_id in departments_2021_ids:
            ten_year_budgets.loc[(ten_year_budgets['department_number']==dept_id), 'department_description'] = departments_2021[departments_2021['department_number']==dept_id]['department_description'].values

        # set desire column order
        cols = ['budget_year', 'fund_type', 'fund_code', 'fund_description', 'department_number', 'department_description',
                'approp_authority', 'approp_auth_description', 'approp_account', 'approp_account_description', 'amount']

        # return value in correct order and convert it to json
        return ten_year_budgets[cols].to_json(orient='records')

        
#if __name__ == '__main__':

#    with open('ten_year_budgets.json', 'w') as json_file:
 #       json.dump(Extract().extract_budgets, json_file)
