import React, { useState, useEffect } from 'react';
import { Card } from '@blueprintjs/core';

import SelectColumnForm from '../Datasets/Forms/SelectColumnForm';
import './DatasetPlot.css';

const DatasetPlot = (props) => {
  const [columnToPlot, setColumnToPlot] = useState(
    props.columns.length > 0 ? props.columns[0] : undefined
  );

  const handleColumnSelect = (column, e) => setColumnToPlot(column);

  return(
    <Card id="dataset-plot">
      <div id="header">
        <span id="title">{props.title}</span>
        <div id="select-column-wrapper">
          <SelectColumnForm 
            columns={props.columns}
            column={columnToPlot}
            handleColumnSelect={handleColumnSelect}/>
        </div>
      </div>
    </Card>
  );
};

export default DatasetPlot;