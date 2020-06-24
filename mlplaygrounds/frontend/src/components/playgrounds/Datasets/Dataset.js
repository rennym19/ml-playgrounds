import React, { useState, useEffect } from 'react';
import { Spinner } from '@blueprintjs/core';
import { faListOl, faColumns, faPercentage } from '@fortawesome/free-solid-svg-icons';

import DatasetsAPIService from '../../../shared/data/api/Datasets';
import ModelsAPIService from '../../../shared/data/api/Models';
import DatasetInfo from './Cards/DatasetInfo';
import DatasetModels from './Cards/DatasetModels';
import DatasetPlot from './Plots/DatasetPlot';
import LabelDistribution from './Plots/LabelDistribution';
import UserWelcomeCard from '../Users/UserWelcomeCard';
import './Dataset.css';

const Dataset = (props) => {
  const [dataset, setDataset] = useState(undefined);
  const [models, setModels] = useState(undefined);

  useEffect(() => {
    getDataset();
  }, [props.selectedDataset]);

  const getDataset = () => {
    const datasetId = props.selectedDataset.uid;
    const userToken = props.authService.token;

    DatasetsAPIService.getDataset(
      datasetId,
      userToken,
      (res) => {
        setDataset(res);
        if (models !== undefined) {
          setModels(undefined);
        }

        ModelsAPIService.getModels(
          userToken,
          datasetId,
          (res) => { setModels(res); }
        );
      }
    );
  }

  const getModels = () => {

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