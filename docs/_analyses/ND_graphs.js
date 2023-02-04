var MAP = {
	x: ['2015', '2016', '2017', '2018', '2019', '2020', '2021'],
	y: [1085776090, 1162904244, 1216183814, 1222239306, 1163970291, 1274342537, 1370853176],
	name: 'MAP',
	type: 'scatter'
};

var ADM = {
	x: ['2015', '2016', '2017', '2018', '2019', '2020', '2021'],
	y: [69540499, 140558672, 104282126, 119848717, 110757865, 100102904, 105396134],
	yaxis: 'y2',
	name: 'ADM',
	type: 'scatter'
};

var CHIP = {
	x: ['2015', '2016', '2017', '2018', '2019', '2020', '2021'],
	y: [9929054, 8898918, 9496780, 9503994, 10169390, 3638180, 2065430],
	yaxis: 'y2',
	name: 'CHIP',
	type: 'scatter'
};

var data = [MAP, ADM, CHIP];

var layout = {
    title: 'State FMR Total Computable Amounts',
    height: 640,
    yaxis: {
        title: 'MAP',
		side: 'left'
    },
    yaxis2: {
        title: 'ADM & CHIP',
        overlaying: 'y',
        side: 'right'
    }
};

Plotly.newPlot('fmr_plot', data, layout);