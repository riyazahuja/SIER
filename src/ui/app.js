// Fetch the stock data from the JSON file
fetch('../../data/processed/IBM_full.json')
    .then(response => response.json())
    .then(data => {
        // Assuming the data format is the same as the one provided in the question
        const stockData = data; // now stockData holds your JSON data

        // After fetching the data and within the .then() block where you have your data

// Prepare the data for the closing prices line chart
const dates = Object.keys(stockData.IBM).reverse();
const closingPrices = dates.map(date => stockData.IBM[date].close);

// Prepare the data for the volume bar chart
const volumes = dates.map(date => stockData.IBM[date].volume);

// Setting up the mixed chart
const ctx = document.getElementById('chartContainer').getContext('2d');
const mixedChart = new Chart(ctx, {
    type: 'bar', // Base type is bar chart
    data: {
        labels: dates,
        datasets: [
            {
                label: 'IBM Closing Prices',
                type: 'line', // Specify the type for this dataset as line
                data: closingPrices,
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.5)',
                yAxisID: 'y-axis-1',
                tension: 0.1
            },
            {
                label: 'IBM Trading Volume',
                type: 'bar', // Specify the type for this dataset as bar
                data: volumes,
                backgroundColor: 'rgba(153, 102, 255, 0.5)',
                yAxisID: 'y-axis-2'
            }
        ]
    },
    options: {
        scales: {
            'y-axis-1': {
                type: 'linear',
                display: true,
                position: 'left',
                title: {
                  text: 'Closing Price ($)',
                  display: true
                },
                // if the volumes have much larger values than prices
                // you may want to start this axis from 0 to compare trends more easily
                beginAtZero: false, 
            },
            'y-axis-2': {
                type: 'linear',
                display: true,
                position: 'right',
                title: {
                  text: 'Volume',
                  display: true
                },
                // align the volume axis to the right
                grid: {
                    drawOnChartArea: false // only show the grid for this axis
                },
                beginAtZero: true, // it makes sense for volume to start at 0
            }
        }
    }
});

    })
    .catch(error => {
        console.error("Error loading stock data:", error);
    });
