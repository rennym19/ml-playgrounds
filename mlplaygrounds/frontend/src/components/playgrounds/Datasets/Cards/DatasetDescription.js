import React, { useState } from 'react';
import { Card, Elevation } from '@blueprintjs/core';

import './DatasetDescription.css';

const DatasetDescription = (props) => {
  return (
    <Card id="description-card" elevation={Elevation.ONE}>
      <span id="title">Dataset Description</span>
    </Card>
  );
};

export default DatasetDescription;