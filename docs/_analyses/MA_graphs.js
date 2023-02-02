var MAP = {
	x: ['2015', '2016', '2017', '2018', '2019', '2020', '2021'],
	y: [15378247995, 16990908511, 17120855005, 17655414020, 17412670180, 17967352114, 19909697384],
	name: 'MAP',
	type: 'scatter'
};

var ADM = {
	x: ['2015', '2016', '2017', '2018', '2019', '2020', '2021'],
	y: [785793341, 874582346, 1026999620, 1044441404, 1226859764, 960363378, 1154382502],
	yaxis: 'y2',
	name: 'ADM',
	type: 'scatter'
};

var CHIP = {
	x: ['2015', '2016', '2017', '2018', '2019', '2020', '2021'],
	y: [309676728, 414452899, 481197972, 490393108, 511619150, 560477142, 515661763],
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