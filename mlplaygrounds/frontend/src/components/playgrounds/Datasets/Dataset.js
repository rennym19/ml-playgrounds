import React, { useState, useEffect } from 'react';
import { Spinner } from '@blueprintjs/core';
import { faListOl, faColumns, faPercentage } from '@fortawesome/free-solid-svg-icons';

import DatasetsAPIService from '../../../shared/data/api/Datasets';
import DatasetInfo from './Cards/DatasetInfo';
import DatasetDescription from './Cards/DatasetDescription';
import DatasetPlot from '../Plots/DatasetPlot';
import LabelDistribution from './Plots/LabelDistribution';
import UserWelcomeCard from '../Users/UserWelcomeCard';
import './Dataset.css';

const Dataset = (props) => {
  const [dataset, setDataset] = useState(undefined);

  useEffect(() => {
    getDataset();
  }, [props.selectedDataset]);

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
          <UserWelcomeCard
            id="user-card"
            username={props.authService.username}/>
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
              label={dataset.label}
              columns={
                dataset.features !== undefined && dataset.label !== undefined
                  ? dataset.features.concat([dataset.label])
                  : dataset.features
              }/>
          </div>
          <div id="dataset-data">
            <LabelDistribution
              label={dataset.label} />
          </div>
          <div id="dataset-description">
            <DatasetDescription />
          </div>
        </div>
      : <div id="loading">
          <Spinner />
        </div>
  );
};

export default Dataset;