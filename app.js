'use strict';


//import { Chart, ArcElement, Tooltip, LinearScale, TimeScale} from 'chart.js';
//Chart.register(ArcElement, Tooltip, LinearScale, TimeScale);



import Chart from 'chart.js/auto';
import 'chartjs-adapter-date-fns';


var chart_body = new Chart(
    document.getElementById('acquisitions'),
    {
        type: 'line',
        data: {
            //datasets: datasets_prepare
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    type: 'time',
                    /*time: {
                        //unit: 'hour',
                        //min: minDate,
                        //max: maxDate,
                        //displayFormats: {
                        //    hour: 'HH'
                        //},
                        parser: function (utcMoment) {
                            return utcMoment.utcOffset('+0800');
                        }                
                    }*/
                }
            }
              
        }
    }
);

fetch("all_stats.json")
    .then((response) => response.json())
    .then((data) => {
        console.log(data);


        //console.log(data_array);
        var datasets_prepare = [];
        var count = 0;
        for (const [key, value] of Object.entries(data["SCORE_HISTORY"])) {
            count += 1;
            if (count >7) {break}
            console.log(count);
            var data_array = [];
            for (var i = 0; i < value.length; i++) {
                //console.log(value[i]);
                data_array.push({ "x": value[i]["TIME"] * 1000, "y": value[i]["SCORE"] });
            }
            datasets_prepare.push({
                data: data_array,
                stepped: true,
                label: data["PROFILES"][key.toString()]["DATA"]['username'] + "#" + data["PROFILES"][key.toString()]["DATA"]['discriminator'],
                hidden: count > 7
            })

        }

        console.log(datasets_prepare);
        chart_body.data.datasets = datasets_prepare;
        chart_body.update();


    });
