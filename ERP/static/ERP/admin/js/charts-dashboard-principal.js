/**
 * Created by bamaa on 26/09/17.
 */
/**
 * Created by bamaa on 25/09/17.
 */

var $j = jQuery.noConflict();

$j(document).on('ready', main_consulta);

var datosJson
var newToken


function main_consulta() {
    $j.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if(settings.type == "POST"){
				xhr.setRequestHeader("X-CSRFToken", $j('[name="csrfmiddlewaretoken"]').val());
                //xhr.overrideMimeType( "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet; charset=utf-8" );
			}
            if(settings.type == "GET"){
				xhr.setRequestHeader("X-CSRFToken", $j('[name="csrfmiddlewaretoken"]').val());
                //xhr.overrideMimeType( "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet; charset=utf-8" );
			}
		}
	});
    callGraphicOne();


}


function callGraphicOne() {
    //$j.get("/obras/register_by_token", function(respu) {
        var projectID = parseInt(document.getElementById("projectID").value);
        var ajax_data = {
            "project_id": projectID
        };

        $j.ajax({
            url: '/reporting/get_dashboard_by_project',
            type: 'get',
            data: ajax_data,
            success: function(data) {
                datosJson=data;
                Series = obtenSeries_Mensual_Grupo(data.schedule);
                graficaUno("",Series.serie,Series.categoria,"","","");
                //putDatosGrafica("GC_Basica");
            },
            error: function(data) {
                alert('se generó un error!!! ' + data.error);
                //$j("#ajaxProgress").hide();
            }
        });
    //});
}



function obtenSeries_Mensual_Grupo(datosJson2) {
    var Series = {
      'serie': [],
      'categoria': []
    };
    var datos=[];
    var nombres=[];
    var arrMeses=[];
    var arrMesesAnio=[];
    var indiceArrMes = 0; // este índice lo definimos para poder controlar el llenado del arrego de meses
    var nombreMesAnio="";


    datos["Total Programado"] = [];
    datos["Avance Financiero"] = [];
    datos["Avance Físico"] = [];

    nombres.push("Total Programado");
    nombres.push("Avance Financiero");
    nombres.push("Avance Físico");

    for (var i = 0; i <= datosJson2.length-1; i++) {
        indiceArrMes = 0; // lo inicializamos en cero para que cada cambio de año se agregen los meses que correspondan
        for (var j = 0; j <= datosJson2[i].months.length-1; j++) {

            datos["Total Programado"].push(datosJson2[i].months[j].accumulated_programmed)
            datos["Avance Financiero"].push(datosJson2[i].months[j].accumulated_paid_estimate)
            datos["Avance Físico"].push(datosJson2[i].months[j].accumulated_total_estimate)

            nombreMesAnio = datosJson2[i].months[j].month+"-"+datosJson2[i].year; //datosJson2[i].months[j].category[k].name;
            //uso arrMesesAnio para identificar si el mes+anio ya estan en el arreglo y poder agregar o no el mes a arrMeses
            //esto por que en algunos casos no vienen todos los meses en el json.
            if (arrMesesAnio[nombreMesAnio]==undefined){
                arrMesesAnio[nombreMesAnio]=[];
                arrMeses.push(datosJson2[i].months[j].month+"-"+datosJson2[i].year);
            }

        }
    }
    console.log(arrMeses);
    // con el arreglo nombres se recorre el arreglo asociativo para llenar el json de series.
    for (var i = 0; i <= nombres.length-1; i++) {
        Series.serie.push({
            'name': nombres[i],
            'data': datos[nombres[i]]
        });
    }
    Series.categoria = arrMeses;
    return Series;
}




function graficaUno(contenedor,Series,Categorias,titulo,subtitulo,leyenda) {
    Highcharts.chart('container-chart-2', {
        colors: ['#2b908f', '#90ee7e', '#f45b5b', '#7798BF', '#aaeeee', '#ff0066', '#eeaaee',
            '#55BF3B', '#DF5353', '#7798BF', '#aaeeee'
        ],
        chart: {
            type: 'spline',
            marginLeft: 55,
            backgroundColor: {
                linearGradient: {
                    x1: 0,
                    y1: 0,
                    x2: 1,
                    y2: 1
                },
                stops: [
                    [0, '#454e8f'],
                    [1, '#454e8f']
                ]
            },
            exporting: {enabled: false},
            style: {
                fontFamily: '\'Unica One\', sans-serif'
            },
            plotBorderColor: '#606063'
        },
        title: {
            text: '',
            style: {
                color: '#E0E0E3',
                textTransform: 'uppercase',
                fontSize: '20px'
            }
        },
        subtitle: {
            style: {
                color: '#E0E0E3',
                textTransform: 'uppercase'
            }
        },
        xAxis: {
            categories: Categorias,
            gridLineColor: '#707073',
            labels: {
                style: {
                    color: '#E0E0E3'
                }
            },
            lineColor: '#707073',
            minorGridLineColor: '#505053',
            tickColor: '#707073',
            title: {
                style: {
                    color: '#A0A0A3'

                }
            }
        },
        yAxis: {
            gridLineColor: '#707073',
            labels: {
                style: {
                    color: '#E0E0E3'
                }
            },
            lineColor: '#707073',
            minorGridLineColor: '#505053',
            tickColor: '#707073',
            tickWidth: 1,
            title: {
                style: {
                    color: '#A0A0A3'
                }
            }
        },
        tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.85)',
            style: {
                color: '#F0F0F0'
            }
        },
        plotOptions: {
            series: {
                dataLabels: {
                    color: '#B0B0B3'
                },
                marker: {
                    lineColor: '#333'
                }
            },
            boxplot: {
                fillColor: '#505053'
            },
            candlestick: {
                lineColor: 'white'
            },
            errorbar: {
                color: 'white'
            }
        },
        legend: {
            enabled: false,
            itemStyle: {
                color: '#E0E0E3'
            },
            itemHoverStyle: {
                color: '#FFF'
            },
            itemHiddenStyle: {
                color: '#606063'
            }
        },
        credits: {
            style: {
                color: '#666'
            }
        },
        labels: {
            style: {
                color: '#707073'
            }
        },

        drilldown: {
            activeAxisLabelStyle: {
                color: '#F0F0F3'
            },
            activeDataLabelStyle: {
                color: '#F0F0F3'
            }
        },

        navigation: {
            buttonOptions: {
                symbolStroke: '#DDDDDD',
                theme: {
                    fill: '#505053'
                }
            }
        },

        // scroll charts
        rangeSelector: {
            buttonTheme: {
                fill: '#505053',
                stroke: '#000000',
                style: {
                    color: '#CCC'
                },
                states: {
                    hover: {
                        fill: '#707073',
                        stroke: '#000000',
                        style: {
                            color: 'white'
                        }
                    },
                    select: {
                        fill: '#000003',
                        stroke: '#000000',
                        style: {
                            color: 'white'
                        }
                    }
                }
            },
            inputBoxBorderColor: '#505053',
            inputStyle: {
                backgroundColor: '#333',
                color: 'silver'
            },
            labelStyle: {
                color: 'silver'
            }
        },

        navigator: {
            handles: {
                backgroundColor: '#666',
                borderColor: '#AAA'
            },
            outlineColor: '#CCC',
            maskFill: 'rgba(255,255,255,0.1)',
            series: {
                color: '#7798BF',
                lineColor: '#A6C7ED'
            },
            xAxis: {
                gridLineColor: '#505053'
            }
        },

        scrollbar: {
            barBackgroundColor: '#808083',
            barBorderColor: '#808083',
            buttonArrowColor: '#CCC',
            buttonBackgroundColor: '#606063',
            buttonBorderColor: '#606063',
            rifleColor: '#FFF',
            trackBackgroundColor: '#404043',
            trackBorderColor: '#404043'
        },

        // special colors for some of the
        legendBackgroundColor: 'rgba(0, 0, 0, 0.5)',
        background2: '#505053',
        dataLabelsColor: '#B0B0B3',
        textColor: '#C0C0C0',
        contrastTextColor: '#F0F0F3',
        maskColor: 'rgba(255,255,255,0.3)',

        series: Series

    });
}
