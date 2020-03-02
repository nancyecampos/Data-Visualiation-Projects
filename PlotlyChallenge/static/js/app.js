// function to build out plots
function getPlot(id) {
  // pull in data from json file (not in the same folder, specify file path)
  d3.json("../samples.json").then((data)=> {
      console.log(data)

      var wfreq = data.metadata.map(d => d.wfreq)
      console.log(`Washing Frequency: ${wfreq}`)
      
      var samples = data.samples.filter(s => s.id.toString() === id)[0];
      
      console.log(samples);

      // Filter out the top 10
      var samplevalues = samples.sample_values.slice(0, 10).reverse();
      var OTU_top = (samples.otu_ids.slice(0, 10)).reverse();
      var OTU_id = OTU_top.map(d => "OTU " + d)


      // get the top 10 labels for the bar plot
      var labels = samples.otu_labels.slice(0, 10);
      var trace = {
          x: samplevalues,
          y: OTU_id,
          text: labels,
          marker: {
            color: 'rgb(17,89,86)'},
          type:"bar",
          orientation: "h",
      };

      // create data variable
      var data = [trace];

      // create layout variable to set plots layout
      var layout = {
          title: "Top 10 OTU",
          yaxis:{
              tickmode:"linear",
          },
          margin: {
              l: 100,
              r: 100,
              t: 100,
              b: 30
          }
      };

      // populate the bar plot
      Plotly.newPlot("bar", data, layout);

    
      // bubble chart
      var trace1 = {
          x: samples.otu_ids,
          y: samples.sample_values,
          mode: "markers",
          marker: {
              size: samples.sample_values,
              color: samples.otu_ids
          },
          text: samples.otu_labels

      };

      // set the layout for the bubble plot
      var layout_b = {
          xaxis:{title: "OTU ID"},
          height: 600,
          width: 1000
      };

      // creating data variable 
      var data1 = [trace1];

      // populate the bubble plot
      Plotly.newPlot("bubble", data1, layout_b); 
    });
}  
// function to pull in data
function getInfo(id) {
  // read the json file to get data
  d3.json("../samples.json").then((data)=> {
      
      // get the metadata info for the demographic panel
      var metadata = data.metadata;

      console.log(metadata)

      // filter meta data info by id
      var result = metadata.filter(meta => meta.id.toString() === id)[0];

      // select demographic panel to put data
      var demographicInfo = d3.select("#sample-metadata");
      
      // reset the demographic info panel each time before getting new id info
      demographicInfo.html("");

      // grab demographic data for each id and append the info to the panel using the html formatting 
      Object.entries(result).forEach((key) => {   
              demographicInfo.append("h5").text(key[0].toUpperCase() + ": " + key[1] + "\n");    
      });
  });
}

// create a function to change info with each id
function optionChanged(id) {
  getPlot(id);
  getInfo(id);
}

// create a function to populate the inital data
function init() {
  // select dropdown menu in html 
  var dropdown = d3.select("#selDataset");

  // read the data from json rile
  d3.json("../samples.json").then((data)=> {
      console.log(data)

      // populate the data from the id into the dropdown menu
      data.names.forEach(function(name) {
          dropdown.append("option").text(name).property("value");
      });

      // use functions above to populate the data and the plots onto the html page
      getPlot(data.names[0]);
      getInfo(data.names[0]);
  });
}

init();