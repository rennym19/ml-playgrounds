import React, { useState, useEffect } from 'react';
import { faListOl, faColumns, faPercentage } from '@fortawesome/free-solid-svg-icons';

import DatasetsAPIService from '../../../shared/data/api/Datasets';
import DatasetInfo from './Cards/DatasetInfo';
import DatasetPlot from '../Plots/DatasetPlot';
import './Dataset.css';

const Dataset = (props) => {
  const [dataset, setDataset] = useState(undefined);

  useEffect(() => {
    getDataset();
  }, [dataset]);

  const getDataset = () => {
    DatasetsAPIService.getDataset(
      props.selectedDataset.uid,
      props.authService.token,
      (res) => { setDataset(res); }
    );
  }

  return (
    dataset !== undefined 
      ? <div id="dataset">
          <DatasetInfo
            id="records-card"
            title="Number of Records"
            value={dataset.num_records}
            iconBackground="#87409D"
            icon={faListOl} />
          <DatasetInfo
            id="features-card"
            title="Number of Features"
            value={dataset.features.length}
            iconBackground="#1266D8"
            icon={faColumns} />
          <DatasetInfo
            id="nan-card"
            title="NaN Percentage"
            value={String(dataset.not_assigned_pct) + "%"}
            iconBackground="#56CDA5"
            icon={faPercentage} />
          <div id="data-visualization">
            <DatasetPlot
              title={dataset.name}
              columns={dataset.features}/>
          </div>
        </div>
      : <div id="loading">Loading</div>
  );
};

export default Dataset;