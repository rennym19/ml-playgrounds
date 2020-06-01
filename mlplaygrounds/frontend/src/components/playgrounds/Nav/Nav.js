import React from 'react';
import { useSpring, animated } from 'react-spring'
import { Navbar, Alignment, Button } from '@blueprintjs/core'

import './Nav.css'

function Nav(props) {
  const btnAnimation = useSpring({opacity: !props.showNavbarAddBtn ? 1 : 0})

  return (
    <Navbar>
      <Navbar.Group align={Alignment.LEFT}>
        <Navbar.Heading>ML Playgrounds</Navbar.Heading>
      </Navbar.Group>
      <Navbar.Group align={Alignment.RIGHT}>
        <animated.div style={btnAnimation}>
          <Button
            id="add-dataset-navbar-btn"
            outlined={true}
            className={props.showNavbarAddBtn ? "non-clickable" : ""}
            text="Add Dataset"/>
        </animated.div>        
        <Navbar.Divider />
        <Button className="bp3-minimal" text={props.username}/>
        <Button className="bp3-minimal" text="Logout" onClick={props.logout} />
      </Navbar.Group>
    </Navbar>
  )
}

export default Nav