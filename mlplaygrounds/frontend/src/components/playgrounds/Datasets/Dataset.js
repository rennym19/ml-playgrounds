import React, { useState, useEffect } from 'react';

import DatasetsAPIService from '../../../shared/data/api/Datasets';
import './Dataset.css';

const Dataset = (props) => {
  const [dataset, setDataset] = useState(undefined);

  useEffect(() => {
    getDataset();
  }, []);

  const getDataset = () => {
    DatasetsAPIService.getDataset(
      props.selectedDataset.uid,
      props.authService.token,
      (res) => { setDataset(res); }
    );
  }

  return (
    <h1>Hello</h1>
  );
};

export default Dataset;