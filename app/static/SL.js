
$(document).ready(function () {
    function handleSLResponse(response, status, xhr){
        //console.log(response, status, xhr)
        console.log(response)
        let sl1 = response.yhat
        $("#SLResults").empty();
        //$("#SLLevel").text(JSON.stringify(sl1));

        for(let i in sl1) {
            console.log(i+ " " +sl1[i])
            $("#SLResults").append(i+ " " +sl1[i]+ "<br>")
        };
        //return sl1
        renderChart(sl1);
    };

    function SLButtonClicked(event) {
        var var1 = '/'
        var var2 = '/sl'

        $.getJSON(var2, handleSLResponse);
    };

    $("#SLButton").click(SLButtonClicked);

    function renderChart(sl1) {
        Highcharts.chart('container', {
            chart: {
                type: 'line'
            },
            title: {
                text: 'Mean Global Sea Level'
            },
            subtitle: {
                text: ''
            },
            xAxis: {
                categories: Object.keys(sl1)

            },
            yAxis: {
                title: {
                    text: 'difference(mm)'
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
                name: 'sl1',
                data: Object.values(sl11)
            }, {
                name: 'Baseline',
                data: [3.9, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8]
            }]
        });
    }

})