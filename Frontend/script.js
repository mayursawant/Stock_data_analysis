document.addEventListener('DOMContentLoaded', () => {
    const searchBar = document.getElementById('search-bar');
    const searchButton = document.getElementById('search-button');
    const intervalSelect = document.getElementById('interval');
    const indicatorSelect = document.getElementById('indicator-select');
    const overlayCheckbox = document.getElementById('overlay');
    const getIndicatorChart = document.getElementById('get-indicator-chart');

    const chartContainer = document.getElementById('chart-container');
    let chart;
    let indicatorChart;  // for the indicator chart
    const indicatorChartContainer = document.getElementById('indicator-chart-container');

    async function fetchData(url) {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return await response.json();
        } catch (error) {
            console.error('There has been a problem with your fetch operation:', error);
        }
    }

    function createChart(data) {
        chart = Highcharts.stockChart(chartContainer, {
            rangeSelector: {
                selected: 1
            },
            title: {
                text: 'Stock Price Candlestick Chart'
            },
            series: [{
                type: 'candlestick',
                name: 'Stock Price',
                data: data,
                tooltip: {
                    valueDecimals: 2
                }
            }]
        });
    }

   function createIndicatorChart(data, seriesName = 'Indicator') {
       if(indicatorChart) {
           indicatorChart.addSeries({
               name: seriesName,
               data: data,
               tooltip: {
                   valueDecimals: 2
               },
               color: 'red',
               dashStyle: 'longdash',
           });
       } else {
           console.error('No indicator chart to overlay data onto');
       }
   }

    function createSeparateIndicatorChart(data, seriesName = 'Indicator') {
        indicatorChart = Highcharts.chart(indicatorChartContainer, {
            title: {
                text: 'Indicator Chart'
            },
            xAxis: {
                type: 'datetime'
            },
            series: [{
                name: seriesName,
                data: data,
                tooltip: {
                    valueDecimals: 2
                },
                color: 'red',
                dashStyle: 'longdash',
            }]
        });
    }

    function createIndicatorTable(data) {
        const tableContainer = document.getElementById('table-container');
        tableContainer.innerHTML = '';

        if (data && data.length > 0) {
            const table = document.createElement('table');
            table.classList.add('indicator-table');

            const headerRow = document.createElement('tr');
            const headers = Object.keys(data[0]);
            headers.forEach(header => {
                const th = document.createElement('th');
                th.innerText = header;
                headerRow.appendChild(th);
            });
            table.appendChild(headerRow);

            data.forEach(rowData => {
                const row = document.createElement('tr');
                headers.forEach(header => {
                    const td = document.createElement('td');
                    td.innerText = rowData[header];
                    row.appendChild(td);
                });
                table.appendChild(row);
            });

            tableContainer.appendChild(table);
        } else {
            tableContainer.innerText = 'No data available to display';
        }
    }
    
    
    searchButton.addEventListener('click', async () => {
        const symbol = searchBar.value;
        const interval = intervalSelect.value;
        const indicator = indicatorSelect.value;

        const data = await fetchData(`http://3.84.81.214:5000/process_data/${symbol}/${encodeURIComponent(interval)}`);
        if(data && data.length > 0) {
            createChart(data);
        } else {
            console.error('No data available to plot the chart');
        }
     
        const indicatorData = await fetchData(`http://3.84.81.214:5000/indicator_table/${symbol}/${encodeURIComponent(interval)}/${indicator}`);

        if(indicatorData && indicatorData.length > 0) {
            createIndicatorTable(indicatorData);
        } else {
            const messageElement = document.getElementById('message');
            messageElement.innerText = 'No data available to display';
        }
    });

    
    getIndicatorChart.addEventListener('click', async () => {
    const symbol = searchBar.value;
    const interval = intervalSelect.value;
    const indicator = indicatorSelect.value;

    const indicatorData = await fetchData(`http://3.84.81.214:5000/indicator_plot/${symbol}/${encodeURIComponent(interval)}/${indicator}`);
    
    const messageElement = document.getElementById('message');
    
    if(indicatorData && indicatorData.length > 0) {
        if (overlayCheckbox.checked) {
            createIndicatorChart(indicatorData, indicator.toUpperCase());
        } else {
            createSeparateIndicatorChart(indicatorData, indicator.toUpperCase());
        }
        messageElement.innerText = '';
    } else {
         messageElement.innerText = 'Enough data points not available to plot the indicator';
        }
    });
});
