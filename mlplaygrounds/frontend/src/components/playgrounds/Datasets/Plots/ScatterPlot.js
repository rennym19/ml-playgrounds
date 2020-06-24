import React, { useState, useEffect } from 'react';
import { Scatter } from 'react-chartjs-2';

import rainbow from '../../../../shared/colors/generator';

const formatScatterData = (datasets) => {
  const formattedDatasets = [];

  let counter = 1;
  Object.getOwnPropertyNames(datasets).forEach((name) => {
    const color = rainbow(counter, 1);
    counter += 1;

    formattedDatasets.push({
      label: name,
      borderColor: `rgba(${color.r}, ${color.g}, ${color.b}, 0.4)`,
      backgroundColor: `rgba(${color.r}, ${color.g}, ${color.b}, 0.4)`,
      borderWidth: 0,
      data: datasets[name]
    });
  });

  return { datasets: formattedDatasets };
};

const ScatterPlot = (props) => {
  const [formattedData, setFormattedData] = useState(undefined);

  useEffect(() => {
    if (props.data !== undefined)
      setFormattedData(formatScatterData(props.data));
  }, [props.data]);

  return (
    <>
      {
        formattedData
          ? <Scatter
              data={formattedData}
              options={props.options} />
          : <></>
      }
    </>
  );
};

export default ScatterPlot;