// pulling full json file
// initiate empty array to create new object
var budget2021 = [];

// extract data if it's from 2021
d3.json("static/data/ten_year_budgets.json", function(err, data) {
    if(err) console.log("error fetching data: ", err) 
    for (var i = 0; i < data.length; i++) {
        if(data[i].budget_year === 2021) {
            var lineItem2021 = {
                department:data[i].department_description,
                amount:data[i].amount
            };
            // going to push created line item to budget2021
            budget2021.push(lineItem2021);
            console.log(budget2021)
        }
    }
});

// now that we have just the line items from 2021, let's group totals by department & calculate percentage
// calculate total budget to calculate % of totals by department
const totalBudget2021 = budget2021.reduce(function(previous, current) { 
    return previous + current.amount
}, 0);
console.log("Total Chicago 2021 Budget: $", totalBudget2021)
// extract unique department names