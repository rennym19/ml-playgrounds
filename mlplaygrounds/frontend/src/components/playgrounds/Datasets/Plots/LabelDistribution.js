import React from 'react';
import { Card, Elevation } from '@blueprintjs/core';
import { Doughnut } from 'react-chartjs-2';

import './LabelDistribution.css';

const plotOptions = {
  responsive: true,
  maintainAspectRatio: false
};

const LabelDistribution = (props) => {
  let labels = undefined;
  let data = undefined;

  if (props.y_value_counts !== null) {
    const labels = [];
    const counts = [];
    props.y_value_counts.forEach(element => {
      labels.push(element.y);
      counts.push(element.count);
    });

    data = {
      labels: labels,
      datasets: [{
        data: counts,
        backgroundColor: [
          '#FF6384',
          '#36A2EB',
          '#FFCE56'
        ]
      }]
    };
  }

  return (
    <Card id="label-distribution" elevation={Elevation.ONE}>
      <div id="info-wrapper">
        <span id="title">Label</span>
        <span id="value">
          {
            props.label !== null
              ? props.label
              : "No label"
          }  
        </span>
      </div>
      {
        props.label !== null && props.problem_type !== null
          ? props.y_value_counts !== null
              ? <div id="plot-wrapper">
                  <Doughnut
                    data={data}
                    options={plotOptions} />
                </div>
              : <div id="no-label">
                  <span>Could not retrieve label value counts. Try re-uploading your dataset.</span>
                </div>
          : <div id="no-label">
              <span>Seems like you haven't set a label and/or the problem type to your dataset.</span>
            </div>
      }
    </Card>
  );
};

export default LabelDistribution;