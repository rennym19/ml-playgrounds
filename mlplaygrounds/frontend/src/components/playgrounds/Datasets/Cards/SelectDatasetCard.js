import React, { useState } from 'react';
import { Card, Button } from '@blueprintjs/core';

import './SelectDatasetCard.css';
import SelectDatasetForm from '../Forms/SelectDatasetForm';

const SelectDatasetCard = (props) => {
  const [dataset, setDataset] = useState(undefined);

  const handleItemSelect = (dataset, e) => setDataset(dataset);

  const setSelectedDataset = () => {
    props.setSelectedDataset(dataset);
  };

  return (
    <Card id="select-dataset-card">
      <div className="form-wrapper">
        <h1>Select Dataset</h1>
        <div className="form">
          <SelectDatasetForm
            dataset={dataset}
            datasets={props.datasets}
            handleItemSelect={handleItemSelect} />
        </div>
      </div>
      <Button
        id="submit-btn"
        minimal={true}
        outlined={true}
        fill={true}
        type="submit"
        onClick={() => setSelectedDataset()}
        text="Select" />
    </Card>
  );
};

export default SelectDatasetCard;