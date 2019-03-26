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

        $j.ajax({
            url: '/reporting/get_main_dashboard',
            type: 'get',
            success: function(data) {
                datosJson=data;
                setMapa(data);
                for (var i = 0; i <= data.length-1; i++) {
                    $("#cardGrafica"+i).show();
                    $("#tituloGrafica"+i).html('<div class="text-small"><a href="/admin/ERP/project/dashboard/'+data[i].general.project_id+'/">' + data[i].general.project_name + '</a></div>' + '<div class="item-right" style="    top: 2px;"><a href="/admin/ERP/project/dashboard/'+data[i].general.project_id+'/" class="btn btn-raised btn-default btn-xs"><i class="fa fa-tachometer color-danger eliminar" style="margin:0;vertical-align: baseline;"></i> Dashboard<div class="ripple-container"></div></a></div>');

                    setDataCircles(data[i].general.percentaje_estimated, data[i].general.percentaje_paid_estimated,i);
                    Series = obtenSeries_Mensual_Grupo(data[i].schedule);
                    graficaUno("container-chart-"+i, Series.serie, Series.categoria, "", "", "");
                }
            },
            error: function(data) {
var message = 'Ocurrió un error al configurar el proyecto, favor de informar al administrador del sistema el siguiente código de error:\n' + data.status;
            $('#alertModal').find('.modal-body p').text(message);
            $('#alertModal').modal('show')                //$j("#ajaxProgress").hide();
            }
        });
    //});
}

function setDataCircles(porcentaje_fisico, porcentaje_financiero,indice){
    var myCircle = Circles.create({
                id: 'circles-'+indice,
                radius: 50,
                value: porcentaje_fisico,
                maxValue: 100,
                width: 5,
                text: function (value) {
                    return value + '%';
                },
                colors: ['#f1f1f1', '#000'],
                duration: 600,
                wrpClass: 'circles-wrp',
                textClass: 'circles-text',
                valueStrokeClass: 'circles-valueStroke circle-primary',
                maxValueStrokeClass: 'circles-maxValueStroke',
                styleWrapper: true,
                styleText: true
            });
             var myCircle = Circles.create({
                id: 'circles-'+indice+'-'+indice,
                radius: 50,
                value: porcentaje_financiero,
                maxValue: 100,
                width: 5,
                text: function (value) {
                    return value + '%';
                },
                colors: ['#f1f1f1', '#000'],
                duration: 600,
                wrpClass: 'circles-wrp',
                textClass: 'circles-text',
                valueStrokeClass: 'circles-valueStroke circle-primary',
                maxValueStrokeClass: 'circles-maxValueStroke',
                styleWrapper: true,
                styleText: true
            });
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
    Highcharts.chart(contenedor, {
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
                fontSize: '5px'
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
                text: 'Montos',
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


function setMapa(Datos){

     var mapOptions = {
                zoom: 4,
                center: new google.maps.LatLng(19.39068,-99.2837006),
                style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
                mapTypeIds: ['roadmap', 'terrain']
            }
            var map = new google.maps.Map(document.getElementById('map'),
                    mapOptions);


    setMarkers(map,puntosMapa(Datos));

}
function puntosMapa(Datos) {
  var arregloSimple=new Array();
  var arregloDoble=new Array();
    var arregloObjeto = new Object();

    for(var i= 0;i<Datos.length;i++){
        var arregloSimple=new Array();
        arregloSimple.push("<b>Obra:</b>" + Datos[i].general.project_name + " <br> ");
        arregloSimple.push(Datos[i].general.project_latitud);
        arregloSimple.push(Datos[i].general.project_longitud);
        arregloSimple.push(i);
        arregloDoble.push(arregloSimple);
    }
    arregloObjeto = arregloDoble;
    return arregloObjeto;
}

function puntosMapaObra(Datos) {
  var arregloSimple=new Array();
  var arregloDoble=new Array();
    var arregloObjeto = new Object();
    for(var i= 0;i<Datos.obras.length;i++){
        var arregloSimple=new Array();
        arregloSimple.push(Datos.obras[i].identificador_unico+ ", " + Datos.obras[i].estado__nombreEstado);
        arregloSimple.push(Datos.obras[i].latitud);
        arregloSimple.push(Datos.obras[i].longitud);
        arregloSimple.push(i);
        arregloDoble.push(arregloSimple);
    }
    arregloObjeto = arregloDoble;
    return arregloObjeto;
}
function setMarkers(mapa, lugares) {
  var infowindow = new google.maps.InfoWindow();


  for (var i = 0; i < lugares.length; i++) {
    var puntos = lugares[i];
    var myLatLng = new google.maps.LatLng(puntos[1], puntos[2]);
    var marker = new google.maps.Marker({
        position: myLatLng,
        map: mapa,
        icon: '../static/ERP/admin/img/pin4.png',
        title: puntos[0],
        zIndex: puntos[3]
    });

      google.maps.event.addListener(marker, 'click', (function(marker, puntos) {
        return function() {
          infowindow.setContent(puntos[0]);
          infowindow.open(mapa, marker);
        }
      })(marker, puntos));
  }
}