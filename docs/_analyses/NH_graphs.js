var MAP = {
	x: ['2015', '2016', '2017', '2018', '2019', '2020', '2021'],
	y: [1716225884, 1948727991, 2055479922, 2150375296, 1985132112, 2252876680, 2381983996],
	name: 'MAP',
	type: 'scatter'
};

var ADM = {
	x: ['2015', '2016', '2017', '2018', '2019', '2020', '2021'],
	y: [124499881, 127861342, 107919839, 122962190, 142205939, 117649158, 115819830],
	yaxis: 'y2',
	name: 'ADM',
	type: 'scatter'
};

var CHIP = {
	x: ['2015', '2016', '2017', '2018', '2019', '2020', '2021'],
	y: [31986, 13334, 14239, 17643, 13335, 3924, 21395],
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