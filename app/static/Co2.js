
$(document).ready(function () {
    function handleCo2Response(response, status, xhr){
        //console.log(response, status, xhr)
        console.log(response)
        let Co2l = response.yhat
        $("#Co2Results").empty();
        //$("#Co2Level").text(JSON.stringify(Co2l));

        for(let i in Co2l) {
            console.log(i+ " " +Co2l[i])
            $("#Co2Results").append(i+ " " +Co2l[i]+ "<br>")
        };
        //return Co2l
        renderChart(Co2l);
    };

    function Co2ButtonClicked(event) {
        var var1 = '/Co2_dates'
        var var2 = '/Co2'

        $.getJSON(var2, handleCo2Response);
    };

    $("#Co2Button").click(Co2ButtonClicked);

    function renderChart(Co2l) {
        Highcharts.chart('container', {
            chart: {
                type: 'line'
            },
            title: {
                text: 'Predicted Co2 in the Atmosphere'
            },
            subtitle: {
                text: ''
            },
            xAxis: {
                categories: Object.keys(Co2l)

            },
            yAxis: {
                title: {
                    text: 'Co2 (ppm)'
                }
            },
            plotOptions: {
                line: {
                    dataLabels: {
                        enabled: true
                    },
                    enableMouseTracking: true
                }
            },
            series: [{
                name: 'Co2l',
                data: Object.values(Co2l)
            }, {
                name: 'Baseline',
                data: [3.9, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8]
            }]
        });
    }

})