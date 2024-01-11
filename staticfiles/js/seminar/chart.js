var data_json = JSON.parse(document.getElementById('data').innerHTML.replace(/'/g, '"'));

var cardColor = config.colors.cardColor;
var headingColor = config.colors.headingColor;
var axisColor = config.colors.axisColor;
var borderColor = config.colors.borderColor;

console.log(data_json[0]);

function createChart(data, id, name) {
    new ApexCharts(
        document.querySelector(id),
        {
            series: data.series,
            chart: {
                height: 300,
                type: 'area',
                parentHeightOffset: 0,
                parentWidthOffset: 0,
                toolbar: {
                    show: true
                },
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                width: 2,
                curve: 'smooth'
            },
            xaxis: {
                type: 'datetime',
                categories: data.categories,
                axisBorder: {
                    show: false
                },
                axisTicks: {
                    show: false
                },
                labels: {
                    datetimeUTC: false,
                    show: true,
                    style: {
                        fontSize: '13px',
                    }
                }
            },
            colors: data.colors,
            legend: {
                show: true,
                horizontalAlign: 'left',
                position: 'top',
                markers: {
                    height: 8,
                    width: 8,
                    radius: 12,
                    offsetX: -3
                },
                labels: {
                    colors: axisColor
                },
                itemMargin: {
                    horizontal: 10
                }
            },
            yaxis: {
                labels: {
                    show: false,
                    formatter: function(val, index) {
                        return parseFloat(val.toFixed(2));
                    }
                },
            },
            fill: {
                type: 'gradient',
                gradient: {
                    shadeIntensity: 0.6,
                    opacityFrom: 0.5,
                    opacityTo: 0.25,
                    stops: [0, 95, 100]
                }
            },
            grid: {
                borderColor: '#eceef1',
                strokeDashArray: 3,
                padding: {
                    top: -20,
                    bottom: -8,
                    left: -10,
                    right: 8
                }
            },
            tooltip: {
                x: {
                    format: 'dd/MM/yy HH:mm:ss'
                },
            },
        }
    ).render();
}

function createConclusion(data, id, name) {
    new ApexCharts(
        document.querySelector(id),
        {
            chart: {
                height: 200,
                width: 200,
                type: 'donut'
            },
            labels: Object.keys(data.conclusion),
            series: Object.values(data.conclusion),
            colors: data.colors,
            stroke: {
                width: 5,
                colors: [cardColor]
            },
            dataLabels: {
                enabled: false,
                formatter: function (val, opt) {
                    return parseInt(val) + '%';
                }
            },
            legend: {
                show: false
            },
            grid: {
                padding: {
                    top: 0,
                    bottom: 0,
                    right: 15
                }
            },
            states: {
                hover: {
                    filter: { type: 'none' }
                },
                active: {
                    filter: { type: 'none' }
                }
            },
            plotOptions: {
                pie: {
                    donut: {
                        size: '75%',
                        labels: {
                            show: true,
                            value: {
                                fontSize: '1.5rem',
                                fontFamily: 'Public Sans',
                                color: headingColor,
                                offsetY: -15,
                                formatter: function (val) {
                                    return parseFloat(val) + '%';
                                }
                            },
                            name: {
                                offsetY: 20,
                                fontFamily: 'Public Sans',
                                fontSize: '0.5rem'
                            },
                            total: {
                                show: true,
                                fontSize: '0.8125rem',
                                color: data.colors[0],
                                label: Object.keys(data.conclusion)[0],
                                formatter: function (w) {
                                    return Object.values(data.conclusion)[0] + '%';
                                }
                            }
                        }
                    }
                }
            }
        },
        
    ).render();
}

function createData(colors, labels, slice0, slice1, chartId, conclusionId, title) {
    const getSeries = () => labels.map(label => ({ name: label, data: [] }));
    var getLabel;

    getLabel = (predictions) => labels[predictions.indexOf(Math.max(...predictions))];

    var categories = [];
    var series = getSeries();
  
    data_json.forEach((item0, index0) => {
        var seriesCounter = labels.reduce((acc, label, index) => ({ ...acc, [label]: 0 }), {});
        item0.data.forEach((item1, index1) => {seriesCounter[getLabel(item1.slice(slice0, slice1))] += 1;});
        for (let i = 0; i < series.length; i++) {
            const serie = series[i];
            const data = seriesCounter[serie.name];
            serie.data.push(data);
        }
        categories.push(item0.created_at);
    });

    function createConclusionData() {
        const entries = series.reduce((sum, item) => sum + item.data.reduce((a, b) => a + b, 0), 0);
        const percentages = series.map((item) => {
            const count = item.data.reduce((sum, count) => sum + count, 0);
            const percentage = (count / entries) * 100;
            return {[item.name]: parseFloat(percentage.toFixed(2))};
        });
        return Object.assign({}, ...percentages);
    }

    const data = {
        colors: colors,
        categories: categories,
        series: series,
        conclusion: createConclusionData(),
    }

    createChart(data, chartId, title);
    createConclusion(data, conclusionId, title);
}

if (data_json.length != 0) {

    createData(
        ['#FF5722', '#4CAF50', '#607D8B', '#FFEB3B', '#9E9E9E', '#2196F3', '#FF9800'],
        ['0-2', '10-20', '21-27', '28-45', '3-9', '46-65', '66-116'],
        0,
        7,
        '#achart',
        '#aconclusion',
        'Age',
    );

    createData(
        ['#1976D2', '#E91E63'],
        ['Female', 'Male'],
        7,
        9,
        '#gchart',
        '#gconclusion',
        'Gender',
    );

    createData(
        ['#FF5722', '#607D8B', '#FFEB3B', '#9E9E9E', '#2196F3', '#FF9800'],
        ['Angry', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise'],
        9,
        15,
        '#echart',
        '#econclusion',
        'Emotion',
    );
}