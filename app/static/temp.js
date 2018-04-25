
$(document).ready(function () {
    function handletempResponse(response, status, xhr){
        //console.log(response, status, xhr)
        console.log(response)
        let temp1 = response.yhat
        $("#TempResults").empty();
        //$("#TempLevel").text(JSON.stringify(temp1));

        for(let i in temp1) {
            console.log(i+ " " +temp1[i])
            $("#TempResults").append(i+ " " +temp1[i]+ "<br>")
        };
        //return temp1
        renderChart(temp1);
    };

    function tempButtonClicked(event) {
        var var1 = '/'
        var var2 = '/temp'

        $.getJSON(var2, handletempResponse);
    };

    $("#TempButton").click(tempButtonClicked);

    function renderChart(temp1) {
        Highcharts.chart('container', {
            chart: {
                type: 'line'
            },
            title: {
                text: 'Mean Global Temp'
            },
            subtitle: {
                text: ''
            },
            xAxis: {
                categories: Object.keys(temp1)

            },
            yAxis: {
                title: {
                    text: 'Temperature in Celcius'
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
                name: 'temp1',
                data: Object.values(temp1)
            }, {
                name: 'Baseline',
                data: [3.9, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8]
            }]
        });
    }

})