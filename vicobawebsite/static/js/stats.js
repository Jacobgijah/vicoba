const renderChart = (labels, data) => {

const ctx = document.getElementById('myChart');

new Chart(ctx, {
   type: 'doughnut',
   data: {
     labels: labels,
     datasets: [{
       label: 'Last 6 months Loans',
       data: data,
       borderWidth: 1
     }]
   },
   options: {
    plugins: {
        title: {
            display: true,
            text: 'Loans per category'
        }
    },
    //  scales: {
    //    y: {
    //      beginAtZero: true
    //    }
    //  }
   }
});

};

const renderChart1 = (labels, data) => {

    const ctx = document.getElementById('myChart1');
    
    new Chart(ctx, {
       type: 'pie',
       data: {
         labels: labels,
         datasets: [{
           label: 'Last 6 months Loans',
           data: data,
           borderWidth: 1
         }]
       },
       options: {
        plugins: {
            title: {
                display: true,
                text: 'Loans per category'
            }
        },
        //  scales: {
        //    y: {
        //      beginAtZero: true
        //    }
        //  }
       }
    });
    
    };

const getChartData = () => {
    console.log("fetching");
    fetch('/loan_category_summary')
        .then((res) => res.json())
        .then((results) => {
        console.log("results", results);
        const category_data = results.loan_category_data;
        const [labels, data] = [
            Object.keys(category_data),
            Object.values(category_data)
        ]

        renderChart(labels, data);
        renderChart1(labels, data);
    })
}

document.onload = getChartData();