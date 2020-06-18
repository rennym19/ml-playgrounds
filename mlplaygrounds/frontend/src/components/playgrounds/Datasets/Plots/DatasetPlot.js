import React, { useState, useEffect } from 'react';
import { Card } from '@blueprintjs/core';

import SelectColumnForm from '../Forms/SelectColumnForm';
import LinePlot from './LinePlot';
import ScatterPlot from './ScatterPlot';
import './DatasetPlot.css';

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
  const [plotData, setPlotData] = useState(undefined);

  useEffect(() => {
    updateColumns();
    dataToPlot();
  }, []);

  useEffect(() => {
    dataToPlot();
  }, [xAxisColumn, yAxisColumn, classificationColumn]);

  useEffect(() => {
    updateColumns();
  }, [props.columns]);

  const updateColumns = () => {
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
  };
  
  const handleXAxisColumnSelect = (column, e) => setXAxisColumn(column);
  const handleYAxisColumnSelect = (column, e) => setYAxisColumn(column);
  const handleClassificationColumnSelect = (column, e) => setClassificationColumn(column);

  const dataToPlot = () => {
    if (xAxisColumn !== undefined && yAxisColumn !== undefined && props.data) {
      if (props.problem_type === 'regression') {
        const data = [];
        const labels = [];

        for (let i=0; i<150; i++) {
          const record = props.data[i];
          const x = record[xAxisColumn];
          const y = record[yAxisColumn];

          data.push({ x, y });
        }

        const sortedData = data.sort((a, b) => (a.x > b.x) ? 1 : ((b.x > a.x) ? -1 : 0));
        for (let i=0; i<sortedData.length; i++) {
          labels.push(`${String(sortedData[i].x)}`);
        }
        setPlotData({
          data: sortedData,
          labels: labels,
          title: `Change in ${yAxisColumn} with respect to ${xAxisColumn}`
        });
      } else if (props.problem_type === 'classification') {
        const datasets = {};
        const addToDatasets = (record, bucketName) => { 
          if (datasets.hasOwnProperty(bucketName))
            datasets[bucketName].push(record);
          else
            datasets[bucketName] = [record];
        };

        for (let i=0; i<150; i++) {
          const record = props.data[i];
          const x = record[xAxisColumn];
          const y = record[yAxisColumn];

          addToDatasets({ x, y }, record[classificationColumn]);
        }
  
        setPlotData(datasets);
      }
    }
  };

  return (
    <Card id="dataset-plot">
      <div id="header">
        <span id="title">{props.title}</span>
          {
            props.problem_type === 'regression' || props.problem_type === 'classification'
              ? <div id="select-columns-wrapper">
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
                    {
                      props.problem_type === 'classification'
                        ? <>
                            <span>Category</span>
                            <SelectColumnForm
                              columns={props.columns}
                              column={classificationColumn}
                              handleColumnSelect={handleClassificationColumnSelect}/>
                          </>
                        : <></>
                    }
                </div>
              : <></>
          }
      </div>
      {
	      props.problem_type !== null
          ? <div id="plot-wrapper">
              {
                props.problem_type === 'regression' || props.problem_type === 'classification'
                  ? props.problem_type === 'regression'
                    ? <LinePlot
                        data={plotData}
                        options={plotOptions}
                        xColumn={xAxisColumn}
                        yColumn={yAxisColumn} />
                    : <ScatterPlot
                        data={plotData}
                        options={plotOptions}    
                        xColumn={xAxisColumn}
                        yColumn={yAxisColumn} />
                  : <span>Only regression and classification problems are valid.</span>
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