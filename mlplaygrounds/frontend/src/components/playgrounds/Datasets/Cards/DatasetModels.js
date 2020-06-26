import React, { useState } from 'react';
import { Card, Elevation, Button } from '@blueprintjs/core';

import ModelDialog from '../../Models/Dialogs/ModelDialog';
import './DatasetModels.css';

const DatasetModels = (props) => {
  const [isModelDialogOpened, setModelDialogOpened] = useState(false);

  let models = undefined;
  if (props.models !== undefined && props.models !== null && props.models.length !== 0) {
    models = [];
    props.models.forEach(element => {
      models.push(<li key={element.uid}>{element.name}</li>);
    });
  }

  return (
    <Card id="models-card" elevation={Elevation.ONE}>
      <ModelDialog
        isOpened={isModelDialogOpened}
        toggleOpened={(e) => setModelDialogOpened(!isModelDialogOpened)}
        authService={props.authService}
        datasetId={props.datasetId}
        features={props.features}
        problemType={props.problemType} />
      <div id="header">
        <span id="title">Models</span>
        <div id="add-model-btn-wrapper">
          <Button
            id="add-model-btn"
            minimal={true}
            outlined={true}
            text={"New Model"}
            onClick={() => setModelDialogOpened(!isModelDialogOpened)}/>
        </div>
      </div>
      {
        props.models !== undefined && props.models !== null && props.models.length !== 0
          ? <div id="models" className="bp3-running-text">
              <ol>{models}</ol>
            </div>
          : <div id="no-models">
              <span>No models created yet</span>
            </div>
      }
    </Card>
  );
};

export default DatasetModels;