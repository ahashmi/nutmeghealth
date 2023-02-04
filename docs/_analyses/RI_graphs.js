var MAP = {
	x: ['2015', '2016', '2017', '2018', '2019', '2020', '2021'],
	y: [2584840295, 2411382026, 2623111291, 2620033271, 2586208738, 2810004409, 3003255442],
	name: 'MAP',
	type: 'scatter'
};

var ADM = {
	x: ['2015', '2016', '2017', '2018', '2019', '2020', '2021'],
	y: [144419143, 215299888, 163239202, 163509707, 179026741, 151429700, 174401320],
	yaxis: 'y2',
	name: 'ADM',
	type: 'scatter'
};

var CHIP = {
	x: ['2015', '2016', '2017', '2018', '2019', '2020', '2021'],
	y: [4742165, 13253050, 13519471, 14080305, 5010442, 2480219, 38424234],
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