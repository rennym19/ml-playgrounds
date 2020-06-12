import React from 'react';
import { Card, Elevation } from '@blueprintjs/core';

import './UserWelcomeCard.css';

const UserWelcomeCard = (props) => {
  return (
    <Card id={props.id} className="user-welcome-card" elevation={Elevation.ONE}>
      <span id="welcome-title">Welcome!</span>
      <span id="welcome-username">{props.username}</span>
    </Card>
  );
};

export default UserWelcomeCard;