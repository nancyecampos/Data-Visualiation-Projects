// from data.js
var tableData = data;
// YOUR CODE HERE!
// Get a reference to the table body
var tbody = d3.select("tbody");
// Loop through dataset to update each cell's text with values from the dataset 
tableData.forEach((ufoReport) => {
    var row = tbody.append("tr");
    Object.entries(ufoReport).forEach(([key, value]) => {
        var cell = row.append("td");
        cell.text(value);
    });
});
// Create button
var ufoButton = data;
var button = d3.select("button");
button.on("click", function() {
    // select input element
    var table = document.getElementById("ufo-table");
    for(var i = table.rows.length - 1; i > 0; i--)
    {
        table.deleteRow(i);
    }
    var inputElement = d3.select("#datetime");
    // get the value property
    var inputValue = inputElement.property("value");
    console.log(inputValue);
    console.log(ufoButton);
    // create filtered data set
    var filteredData = ufoButton.filter(ufo => ufo.datetime === inputValue);
    console.log(filteredData)
    filteredData.forEach((ufoFilter) => {
        var row = tbody.append("tr");
        Object.entries(ufoFilter).forEach(([key, value]) => {
            var cell = row.append("td");
            cell.text(value);
        });
    });
});