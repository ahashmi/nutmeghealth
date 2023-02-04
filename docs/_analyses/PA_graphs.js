var MAP = {
	x: ['2015', '2016', '2017', '2018', '2019', '2020', '2021'],
	y: [23223615661, 27350279117, 28081163760, 29863557849, 32079703325, 34964896749, 37182173112],
	name: 'MAP',
	type: 'scatter'
};

var ADM = {
	x: ['2015', '2016', '2017', '2018', '2019', '2020', '2021'],
	y: [876262086, 870028676, 1002547859, 894756438, 881222787, 1037358355, 1054249179],
	yaxis: 'y2',
	name: 'ADM',
	type: 'scatter'
};

var CHIP = {
	x: ['2015', '2016', '2017', '2018', '2019', '2020', '2021'],
	y: [325176766, 343032036, 414615003, 448166714, 450255000, 458305896, 410058842],
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