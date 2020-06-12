import React from 'react';
import { Card, Elevation } from '@blueprintjs/core';
import { Doughnut } from 'react-chartjs-2';

import './LabelDistribution.css';

const data = {
	labels: [
		'Red',
		'Green',
		'Yellow'
	],
	datasets: [{
		data: [300, 50, 100],
		backgroundColor: [
		'#FF6384',
		'#36A2EB',
		'#FFCE56'
		],
		hoverBackgroundColor: [
		'#FF6384',
		'#36A2EB',
		'#FFCE56'
		]
	}]
};

const plotOptions = {
  maintainAspectRatio: false
};

const LabelDistribution = (props) => {
  return (
    <Card id="label-distribution" elevation={Elevation.ONE}>
      <div id="info-wrapper">
        <span id="title">Label</span>
        <span id="value">
          {
            props.label !== null && props.label !== undefined
              ? props.label
              : "No label"
          }  
        </span>
      </div>
      {
        props.label !== null && props.label !== undefined
          ? <div id="plot-wrapper">
              <Doughnut
                data={data}
                width={"80%"}
                options={plotOptions} />
            </div>
          : <div id="no-label">
              <span>Seems like you haven't set a label to your dataset yet.</span>
            </div>
      }
    </Card>
  );
};

export default LabelDistribution;