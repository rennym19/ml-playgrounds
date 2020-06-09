import React from 'react';
import { Card, Elevation } from '@blueprintjs/core';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCircle } from '@fortawesome/free-solid-svg-icons';

import './DatasetInfo.css';

const DatasetInfo = (props) => {
  return (
    <Card id={props.id} className="info-card" elevation={Elevation.ONE}>
      <div id="info-wrapper">
        <span id="info-title">{props.title}</span>
        <span id="info-val">{props.value}</span>
      </div>
      <div id="icon-wrapper">
        <FontAwesomeIcon
          id="info-icon"
          icon={props.icon}
          color={props.iconBackground}
          mask={faCircle}
          transform="shrink-8"
          size="4x"
          fixedWidth={true} />
      </div>
    </Card>
  );
};

export default DatasetInfo;