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
                /*alert('se generó un error!!! ' + data.error);*/
                alert('Ocurrió un error al configurar el proyecto, favor de informar al administrador del sistema el siguiente código de error: ' + data.status);

                //$j("#ajaxProgress").hide();
            }
        });
    //});
}

function obtenSeries_Mensual_Grupo_auax(datosJson2) {
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



    for (var i = 0; i <= datosJson2.length-1; i++) {
        indiceArrMes = 0; // lo inicializamos en cero para que cada cambio de año se agregen los meses que correspondan
        for (var j = 0; j <= datosJson2[i].months.length-1; j++) {
            // Si el nombre de la categoría aún no existe en el arreglo asociativo, se genera
            if (datos[datosJson2[i].months[j].month+"-"+datosJson2[i].year]==undefined)
            {
                datos[datosJson2[i].months[j].month+"-"+datosJson2[i].year] = []; // se genera el arreglo asociativo con el nombre de la categoria
                nombres.push(datosJson2[i].months[j].month+"-"+datosJson2[i].year); // se agrega el nombre de la categoria al arreglo nombres, para usarlo despúes para recorrer el arreglo asociativo
            }
            for (var k = 0; k <= datosJson2[i].months[j].category.length-1; k++) {
                datos[datosJson2[i].months[j].month+"-"+datosJson2[i].year].push(datosJson2[i].months[j].category[k].total);
                nombreMesAnio = datosJson2[i].months[j].category[k].name;
                //uso arrMesesAnio para identificar si el mes+anio ya estan en el arreglo y poder agregar o no el mes a arrMeses
                //esto por que en algunos casos no vienen todos los meses en el json.
                if (arrMesesAnio[nombreMesAnio]==undefined){
                    arrMesesAnio[nombreMesAnio]=[];
                    arrMeses.push(datosJson2[i].months[j].category[k].name);
                }

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
function obtenSeries_Mensual_Grupo_ant(datosJson2) {
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



    for (var i = 0; i <= datosJson2.length-1; i++) {
        indiceArrMes = 0; // lo inicializamos en cero para que cada cambio de año se agregen los meses que correspondan
        for (var j = 0; j <= datosJson2[i].months.length-1; j++) {
            // Si el nombre de la categoría aún no existe en el arreglo asociativo, se genera
            /*if (datos[datosJson2[i].months[j].month+"-"+datosJson2[i].year]==undefined)
            {
                datos[datosJson2[i].months[j].month+"-"+datosJson2[i].year] = []; // se genera el arreglo asociativo con el nombre de la categoria
                nombres.push(datosJson2[i].months[j].month+"-"+datosJson2[i].year); // se agrega el nombre de la categoria al arreglo nombres, para usarlo despúes para recorrer el arreglo asociativo
            }*/
            for (var k = 0; k <= datosJson2[i].months[j].category.length-1; k++) {

                if (datos[datosJson2[i].months[j].category[k].name]==undefined)
                {
                    datos[datosJson2[i].months[j].category[k].name] = []; // se genera el arreglo asociativo con el nombre de la categoria
                    nombres.push(datosJson2[i].months[j].category[k].name); // se agrega el nombre de la categoria al arreglo nombres, para usarlo despúes para recorrer el arreglo asociativo
                }

                datos[datosJson2[i].months[j].category[k].name].push(datosJson2[i].months[j].category[k].total);
                nombreMesAnio = datosJson2[i].months[j].month+"-"+datosJson2[i].year; //datosJson2[i].months[j].category[k].name;
                //uso arrMesesAnio para identificar si el mes+anio ya estan en el arreglo y poder agregar o no el mes a arrMeses
                //esto por que en algunos casos no vienen todos los meses en el json.
                if (arrMesesAnio[nombreMesAnio]==undefined){
                    arrMesesAnio[nombreMesAnio]=[];
                    arrMeses.push(datosJson2[i].months[j].month+"-"+datosJson2[i].year);
                }

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




function graficaX(contenedor,Series,Categorias,titulo,subtitulo,leyenda) {
            Highcharts.chart('container-chart', {
                chart: {
                    type: 'spline',

                },
                colors: ['#fe887e', '#b389ed', '#00ccff'],
                title: {
                    text: ''
                },
                subtitle: {
                    text: ''
                },
                xAxis: {
                    categories: ['proyecto1', 'proyecto2', 'proyecto3', 'proyecto4', 'proyecto5'],
                    title: {
                        text: null
                    }
                },
                yAxis: {
                    min: 0,
                    title: {
                        text: 'Indicadores',
                        align: 'high'
                    },
                    labels: {
                        overflow: 'justify'
                    }
                },
                tooltip: {
                    valueSuffix: ' millions'
                },
                plotOptions: {
                    bar: {
                        dataLabels: {
                            enabled: true
                        }
                    }
                },
                legend: {
                    layout: 'vertical',
                    align: 'right',
                    verticalAlign: 'top',
                    x: -40,
                    y: 80,
                    floating: true,
                    borderWidth: 1,
                    backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
                    shadow: true
                },
                credits: {
                    enabled: false
                },
                series: [{
                    name: '2012',
                    data: [107, 31, 635, 203, 2]
                }, {
                    name: '2014',
                    data: [133, 156, 947, 408, 6]
                }, {
                    name: '2016',
                    data: [1052, 954, 4250, 740, 38]
                }]
            });
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

function graficaTres(contenedor,Series,Categorias,titulo,subtitulo,leyenda) {
        Highcharts.chart('container-chart-3', {
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

            series: [{
                name: 'Installation',
                data: [43934, 38495, 57177, 38485, 97031, 19833, 29384, 154175]
            }, {
                name: 'Manufacturing',
                data: [374854, 24064, 36474, 29851, 75658, 30282, 38494, 40434]
            }, {
                name: 'Sales & Distribution',
                data: [11744, 39485, 16005, 38475, 20185, 39485, 32147, 39387]
            }, {
                name: 'Project Development',
                data: [null, 373854, 7988, 393, 15112, 47465, 39485, 34227]
            }, {
                name: 'Other',
                data: [12908, 384745, 8105, 47457, 8989, 3748, 18274, 7485]
            }]


        });
}

function graficaCuatro(contenedor,Series,Categorias,titulo,subtitulo,leyenda) {
        Highcharts.chart('container-chart-4', {
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

            series: [{
                name: 'Installation',
                data: [43934, 38495, 57177, 3748, 97031, 374875, 3748, 154175]
            }, {
                name: 'Manufacturing',
                data: [24916, 27485, 29742, 7485, 32490, 37845, 38121, 3746]
            }, {
                name: 'Sales & Distribution',
                data: [11744, 27385, 16005, 7485, 20185, 27484, 32147, 39387]
            }, {
                name: 'Project Development',
                data: [null, null, 37485, 12169, 384575, 22452, 38475, 34227]
            }, {
                name: 'Other',
                data: [12908, 3748, 8105, 38475, 8989, 39485, 18274, 27364]
            }]


        });
}
function graficaCinco(contenedor,Series,Categorias,titulo,subtitulo,leyenda) {
        Highcharts.chart('container-chart-5', {
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

            series: [{
                name: 'Installation',
                data: [43934, 23678, 27485, 69658, 97031, 119931, 17284, 154175]
            }, {
                name: 'Manufacturing',
                data: [24916, 24064, 29742, 19475, 32490, 30282, 38121, 9832]
            }, {
                name: 'Sales & Distribution',
                data: [11744, 17722, 16005, 19771, 20185, 24377, 32147, 39387]
            }, {
                name: 'Project Development',
                data: [null, null, 7988, 12169, 23890, 22452, 345, 34227]
            }, {
                name: 'Other',
                data: [12908, 5948, 234, 11248, 8989, 11816, 18274, 27485]
            }]


        });

}