var MAP = {
	x: ['2015', '2016', '2017', '2018', '2019', '2020', '2021'],
	y: [2477405878.0, 2490164925.0, 2565081585.0, 2686772711.0, 2867136972.0, 3208972015.0, 3344325038.0],
	type: 'scatter'
};

var ADM = {
	x: ['2015', '2016', '2017', '2018', '2019', '2020', '2021'],
	y: [143020754.0, 146278926.0, 169444328.0, 154235161.0, 151862966.0, 146526455.0, 160771800.0],
	type: 'scatter'
};

var CHIP = {
	x: ['2015', '2016', '2017', '2018', '2019', '2020', '2021'],
	y: [13157154.0, 13778397.0, 14373818.0, 17299244.0, 19102859.0, 16934280.0, 18547641.0],
	type: 'scatter'
};

var data = MAP, ADM, CHIP;

Plotly.newPlot('fmr_plot', data);