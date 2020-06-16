import React, { useState } from 'react';
import { Card, Elevation } from '@blueprintjs/core';

import './DatasetModels.css';

const DatasetModels = (props) => {
  let models = undefined;
  if (props.models !== undefined && props.models !== null && props.models.length !== 0) {
    models = array();
    props.models.forEach(element => {
      models.push(<li>{element.name}</li>);
    });
  }

  return (
    <Card id="models-card" elevation={Elevation.ONE}>
      <span id="title">Models</span>
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