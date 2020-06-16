import React, { useState, useEffect } from 'react';
import { Spinner } from '@blueprintjs/core';
import { faListOl, faColumns, faPercentage } from '@fortawesome/free-solid-svg-icons';

import DatasetsAPIService from '../../../shared/data/api/Datasets';
import DatasetInfo from './Cards/DatasetInfo';
import DatasetModels from './Cards/DatasetModels';
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
              problem_type={dataset.problem_type}
	            data={dataset.data}
	            label_data={dataset.label_data}
              columns={
                dataset.features !== undefined && dataset.label !== undefined
                  ? dataset.features.concat([dataset.label])
                  : dataset.features
              }/>
          </div>
          <div id="dataset-label-distribution">
            <LabelDistribution
              label={dataset.label}
              problem_type={dataset.problem_type}
              y_value_counts={dataset.y_value_counts} />
          </div>
          <div id="dataset-models">
            <DatasetModels 
              models={[]}/>
          </div>
        </div>
      : <div id="loading">
          <Spinner />
        </div>
  );
};

export default Dataset;