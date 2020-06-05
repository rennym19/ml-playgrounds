import React from 'react';
import { Card, Button, Text } from '@blueprintjs/core';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFrown } from '@fortawesome/free-solid-svg-icons';

import './NoDatasetsCard.css';

const NoDatasetsCard = (props) => {
  return (
    <Card id="no-datasets-card">
      <FontAwesomeIcon className="card-icon" icon={faFrown} size="6x" />
      <Text className="card-msg">Looks like you don't have any datasets yet</Text>
      <Button
        className="card-btn"
        fill={true}
        minimal={true}
        text="Add Dataset"
        onClick={() => props.toggleShowNavbarAddBtn()} />
    </Card>
  );
};

export default NoDatasetsCard;