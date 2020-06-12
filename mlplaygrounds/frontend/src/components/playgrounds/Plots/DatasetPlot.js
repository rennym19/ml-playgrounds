import React, { useState, useEffect } from 'react';
import { Card } from '@blueprintjs/core';
import {Scatter} from 'react-chartjs-2';

import SelectColumnForm from '../Datasets/Forms/SelectColumnForm';
import './DatasetPlot.css';

const data = {
  labels: ['Scatter'],
  datasets: [
    {
      label: 'My First dataset',
      fill: false,
      backgroundColor: 'rgba(75,192,192,0.4)',
      pointBorderColor: 'rgba(75,192,192,1)',
      pointBackgroundColor: '#fff',
      pointBorderWidth: 1,
      pointHoverRadius: 5,
      pointHoverBackgroundColor: 'rgba(75,192,192,1)',
      pointHoverBorderColor: 'rgba(220,220,220,1)',
      pointHoverBorderWidth: 2,
      pointRadius: 1,
      pointHitRadius: 10,
      data: [
        { x: 65, y: 75 },
        { x: 59, y: 49 },
        { x: 80, y: 90 },
        { x: 81, y: 29 },
        { x: 56, y: 36 },
        { x: 55, y: 25 },
        { x: 40, y: 18 },
      ]
    }
  ]
};

const plotOptions = {
  maintainAspectRatio: false
};

const DatasetPlot = (props) => {
  const [xAxisColumn, setXAxisColumn] = useState(
    props.columns.length > 0 ? props.columns[0] : undefined
  );
  const [yAxisColumn, setYAxisColumn] = useState(props.label);
  
  useEffect(() => {
    setXAxisColumn(props.columns.length > 0 ? props.columns[0] : undefined);
  }, [props.columns]);

  const handleXAxisColumnSelect = (column, e) => setXAxisColumn(column);
  const handleYAxisColumnSelect = (column, e) => setYAxisColumn(column);

  return(
    <Card id="dataset-plot">
      <div id="header">
        <span id="title">{props.title}</span>
        <div id="select-columns-wrapper">
          <div className="select-column-axis">
            <span>X Axis</span>
            <SelectColumnForm 
              columns={props.columns}
              column={xAxisColumn}
              handleColumnSelect={handleXAxisColumnSelect}/>
          </div>
          <div className="select-column-axis">
            <span>Y Axis</span>
            <SelectColumnForm 
              columns={props.columns}
              column={yAxisColumn}
              handleColumnSelect={handleYAxisColumnSelect}/>
          </div>
        </div>
      </div>
      <div id="plot-wrapper">
        <Scatter
          data={data}
          width={"80%"}
          options={plotOptions} />
      </div>
    </Card>
  );
};

export default DatasetPlot;