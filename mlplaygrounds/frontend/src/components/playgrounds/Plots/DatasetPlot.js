import React, { useState, useEffect } from 'react';
import { Card } from '@blueprintjs/core';
import { Scatter, Line } from 'react-chartjs-2';

import SelectColumnForm from '../Datasets/Forms/SelectColumnForm';
import './DatasetPlot.css';

const getLinePlotData = (data, labels, title) => {
  return {
    labels: labels,
    datasets: [
      {
        label: title,
        fill: false,
        lineTension: 0.1,
        backgroundColor: 'rgba(75,192,192,0.4)',
        borderColor: 'rgba(75,192,192,1)',
        borderCapStyle: 'butt',
        borderDash: [],
        borderDashOffset: 0.0,
        borderJoinStyle: 'miter',
        pointBorderColor: 'rgba(75,192,192,1)',
        pointBackgroundColor: '#fff',
        pointBorderWidth: 1,
        pointHoverRadius: 5,
        pointHoverBackgroundColor: 'rgba(75,192,192,1)',
        pointHoverBorderColor: 'rgba(220,220,220,1)',
        pointHoverBorderWidth: 2,
        pointRadius: 1,
        pointHitRadius: 10,
        data: data
      }
    ]
  };
};

const getScatterData = (labels, data) => {
  return {
    labels: labels,
    datasets: [
      {
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
        data: data
      }
    ]
  };
};

const plotOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    xAxes: [{
      gridLines: {
        drawBorder: true,
        display: false
      }
    }],
    yAxes: [{
      gridLines: {
        drawBorder: true,
        display: false
      }
    }]
  }
};

const DatasetPlot = (props) => {
  const [xAxisColumn, setXAxisColumn] = useState(undefined);
  const [yAxisColumn, setYAxisColumn] = useState(undefined);
  const [classificationColumn, setClassificationColumn] = useState(undefined);
  const [plotData, setPlotData] = useState({});

  useEffect(() => {
    if (props.problem_type === 'regression') {
      setXAxisColumn(props.columns.length > 0 ? props.columns[0] : undefined);
      setYAxisColumn(props.label);
    } else if (props.problem_type === 'classification') {
      if (props.columns.length > 1) {
        setXAxisColumn(props.columns[0]);
        setYAxisColumn(props.columns[1]);
      }
      setClassificationColumn(props.label);
    }

    dataToPlot();
  }, []);

  useEffect(() => {
    dataToPlot();
  }, [xAxisColumn, yAxisColumn, classificationColumn]);
  
  useEffect(() => {
    setXAxisColumn(props.columns.length > 0 ? props.columns[0] : undefined);
  }, [props.columns]);

  const handleXAxisColumnSelect = (column, e) => setXAxisColumn(column);
  const handleYAxisColumnSelect = (column, e) => setYAxisColumn(column);

  const dataToPlot = () => {
    if (xAxisColumn !== undefined && yAxisColumn !== undefined) {
      const data = [];
      const labels = [];

      if (props.problem_type === 'regression') {
        if (props.data !== undefined) {
          for (let i=0; i<40; i++) {
            const x = props.data[i][xAxisColumn];
            data.push({
              x: x,
              y: yAxisColumn === props.label ? props.label_data[i] : props.data[i][yAxisColumn]
            });
          }

          const sortedData = data.sort((a, b) => (a.x > b.x) ? 1 : ((b.x > a.x) ? -1 : 0));
          for (let i=0; i<sortedData.length; i++) {
            labels.push(`${String(sortedData[i].x)}`);
          }
          setPlotData(
            getLinePlotData(
              sortedData,
              labels,
              `Change in ${yAxisColumn} with respect to ${xAxisColumn}`
            )
          );
        }
      } else if (props.problem_type === 'classification') {
        setPlotData(getScatterData(data));
      }
    }
  };

  return (
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
      {
	      props.problem_type !== 'regression' || props.problem_type !== 'classification'
        ? <div id="plot-wrapper">
            {
              props.problem_type === 'regression'
                ? <Line 
                    data={plotData}
                    options={plotOptions} />
                : <Scatter
                    data={plotData}
                    options={plotOptions} />
            }
          </div>
        : <div id="unset-problem-type">
            <span>Looks like you haven't set your dataset's problem type.</span>
          </div>
      }
    </Card>
  );
};

export default DatasetPlot;
