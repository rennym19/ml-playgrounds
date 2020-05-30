import React from "react";
import { Navbar, Alignment, Button } from '@blueprintjs/core'

import './Nav.css'

function Nav(props) {
  return (
    <Navbar>
      <Navbar.Group align={Alignment.LEFT}>
        <Navbar.Heading>ML Playgrounds</Navbar.Heading>
      </Navbar.Group>
      <Navbar.Group align={Alignment.RIGHT}>
        <Button id="add-dataset-navbar-btn" outlined={true} text="Add Dataset"/>
        <Navbar.Divider />
        <Button className="bp3-minimal" text={props.username}/>
        <Button className="bp3-minimal" text="Logout" onClick={props.logout} />
      </Navbar.Group>
    </Navbar>
  )
}

export default Nav