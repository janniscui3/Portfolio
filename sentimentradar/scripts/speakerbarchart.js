//AUTOR: Timo Eisert (7470259)

// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

function number_format(number, decimals, dec_point, thousands_sep) {
  // *     example: number_format(1234.56, 2, ',', ' ');
  // *     return: '1 234,56'
  number = (number + '').replace(',', '').replace(' ', '');
  var n = !isFinite(+number) ? 0 : +number,
    prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
    sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
    dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
    s = '',
    toFixedFix = function(n, prec) {
      var k = Math.pow(10, prec);
      return '' + Math.round(n * k) / k;
    };
  // Fix for IE parseFloat(0.55).toFixed(0) = 0;
  s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
  if (s[0].length > 3) {
    s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
  }
  if ((s[1] || '').length < prec) {
    s[1] = s[1] || '';
    s[1] += new Array(prec - s[1].length + 1).join('0');
  }
  return s.join(dec);
}




//##################################################

// Speaker Bar Chart
var ctx5 = document.getElementById("speaker_bar_chart");
var speakerbarchart = new Chart(ctx5, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [{
            
            label: "Anzahl: ",
            backgroundColor: "#4e73df",
            hoverBackgroundColor: "#2e59d9",
            borderColor: "#4e73df",
            speakerids: [],
            data: [],
            picture_links: [],
            order: 1
        }],
    },
    options: {
        maintainAspectRatio: false,
        layout: {
        padding: {
            left: 10,
            right: 25,
            top: 25,
            bottom: 0
        }
        },
        scales: {
        xAxes: [{
            time: {
            unit: 'Anzahl'
            },
            gridLines: {
            display: true,
            drawBorder: true
            },
            ticks: {
            
            },
            maxBarThickness: 25,
        }],
        yAxes: [{
            ticks: {
            min: 0,
            
            
            padding: 10,
            
            },
            gridLines: {
            color: "rgb(234, 236, 244)",
            zeroLineColor: "rgb(234, 236, 244)",
            drawBorder: true,
            borderDash: [2],
            zeroLineBorderDash: [2]
            }
        }],
        },
        legend: {
        display: false
        },
        tooltips: {
        
        
        titleMarginBottom: 10,
        titleFontColor: '#6e707e',
        titleFontSize: 14,
        backgroundColor: "rgb(255,255,255)",
        bodyFontColor: "#858796",
        borderColor: '#dddfeb',
        borderWidth: 1,
        xPadding: 15,
        yPadding: 15,
        displayColors: false,
        caretPadding: 10,
        callbacks: {
            label: function(tooltipItem, chart) {
            var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
            return datasetLabel + number_format(tooltipItem.yLabel)  ;
            }
        }, 
        custom: (tooltipModel, chart) =>{
          
          var picture = document.getElementById("picture")
  
          // Hide if no tooltip
          if (tooltipModel.opacity === 0) {
            picture.style.opacity = 0;
            return;
          }
  
          picture.style.opacity = 1;
          picture.style.top = tooltipModel.y - 100 + "px"
          picture.style.left = tooltipModel.x - 50 + "px"
          
          var tootltipindex = tooltipModel.dataPoints[0].index;
          var link = speakerbarchart.data.datasets[0].picture_links[tootltipindex];
          if(link === ""){
            link = "https://icon-library.com/images/default-profile-icon/default-profile-icon-16.jpg"
          }
          picture.src = link;
  
  
          
  
  
        }
        

      }

      
    }
});



function updateSpeakerBarChart(newids, newlabels, newdata, newlinks){
  speakerbarchart.data.datasets[0].speakerids = newids;
  speakerbarchart.data.labels = newlabels;
  speakerbarchart.data.datasets[0].data = newdata;
  speakerbarchart.data.datasets[0].picture_links = newlinks;
  speakerbarchart.update();
}