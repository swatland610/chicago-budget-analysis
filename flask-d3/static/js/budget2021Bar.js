// pulling full json file
// initiate empty array to create new object
const budget2021 = [];

// extract data if it's from 2021
d3.json("/static/data/ten_year_budgets.json", function(data) {
    for (var i = 0; i < data.length; i++) {
        if(data[i].budget_year === 2021) {
            var lineItem2021 = {
                department:data[i].department_description,
                amount:data[i].department_description
            };
            // going to push created line item to budget2021
            budget2021.push(lineItem2021);
        }
    }
});

