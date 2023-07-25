const renderChart = (labels, data) => {

    const ctx = document.getElementById('myChart');
    
    new Chart(ctx, {
       type: 'bar',
       data: {
         labels: labels,
         datasets: [{
           label: 'Last 6 months Contributions',
           data: data,
           borderWidth: 1
         }]
       },
       options: {
        plugins: {
            title: {
                display: true,
                text: 'Contributions per source'
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
        fetch('/contribution_source_summary')
            .then((res) => res.json())
            .then((results) => {
                console.log("results", results);
            
                renderChart([], []);
        });
    };
    
    document.onload = getChartData();