import React from 'react';
import { useSpring, animated } from 'react-spring';
import { Navbar, Alignment, Button } from '@blueprintjs/core';

import './Nav.css';
import SelectDatasetForm from '../Datasets/Forms/SelectDatasetForm';

const Nav = (props) => {
  const logout = () => { props.authService.logout(); }

  const handleItemSelect = (dataset, e) => props.setSelectedDataset(dataset);

  const btnAnimation = useSpring({opacity: props.showNavbarAddBtn ? 1 : 0});

  return (
    <Navbar>
      <Navbar.Group align={Alignment.LEFT}>
        <Navbar.Heading>ML Playgrounds</Navbar.Heading>
        {
          props.selectedDataset !== undefined
            ? <>
                <Navbar.Divider />
                <SelectDatasetForm
                  dataset={props.selectedDataset}
                  datasets={props.datasets}
                  handleItemSelect={handleItemSelect} />
              </>
            : <></>
        }
      </Navbar.Group>
      <Navbar.Group align={Alignment.RIGHT}>
        <animated.div style={btnAnimation}>
          <Button
            id="add-dataset-navbar-btn"
            outlined={true}
            className={props.showNavbarAddBtn ? "non-clickable" : ""}
            text="Add Dataset"
            onClick={() => props.addDataset()} />
        </animated.div>        
        <Navbar.Divider />
        <Button className="bp3-minimal" text={props.username}/>
        <Button className="bp3-minimal" text="Logout" onClick={logout} />
      </Navbar.Group>
    </Navbar>
  );
};

export default Nav;