import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';

const formatLinePlotData = ({ data, labels, title }) => {
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

const LinePlot = (props) => {
  const [formattedData, setFormattedData] = useState(undefined);

  useEffect(() => {
    if (props.data !== undefined)
      setFormattedData(formatLinePlotData(props.data));
  }, [props.data]);

  return (
    <>
      {
        formattedData
          ? <Line
              data={formattedData}
              options={props.options} />
          : <></>
      }
    </>
  );
};

export default LinePlot;