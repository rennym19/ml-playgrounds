import React, { useState, useEffect } from 'react'
import { Card, Button, Text } from '@blueprintjs/core'
import { useSpring, animated } from 'react-spring'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faFrown } from '@fortawesome/free-solid-svg-icons'

import UsersAPIService from '../../../shared/data/api/Users';
import Nav from '../Nav/Nav'
import DatasetForm from '../Datasets/Forms/DatasetForm'
import './Home.css'

const Home = (props) => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [registrationDate, setRegistrationDate] = useState('');
  const [showNavbarAddBtn, setShowNavbarAddBtn] = useState(true);

  useEffect(() => {
    UsersAPIService.retrieveUserProfile(
      props.authService.token,
      res => {
        setUsername(res.username)
        setEmail(res.email)
        setFirstName(res.first_name)
        setLastName(res.last_ame)
        setRegistrationDate(res.registration_date)
      },
      props.authService.authLogout
    );
  }, []);

  const logout = () => {
    props.authService.logout();
  }

  const toggleShowNavbarAddBtn = () => {
    setShowNavbarAddBtn(!showNavbarAddBtn)
  }

  const noDatasetsCardAnimations = useSpring({
    transform: !showNavbarAddBtn ? 'translate3d(0, 0, 0)' : 'translate3d(-200px, 0, 0)',
    marginRight: !showNavbarAddBtn ? '0px' : '16px'
  })

  const addDatasetCardAnimations = useSpring({
    transform: !showNavbarAddBtn ? 'translate3d(0, 0, 0)' : 'translate3d(+200px, 0, 0)',
    marginLeft: !showNavbarAddBtn ? '0px' : '16px'
  })

  return (
    <div id="Home">
      <Nav
        id="Navbar"
        showNavbarAddBtn={showNavbarAddBtn}
        username={username}
        logout={() => logout()} />
      <div id="Content" className="no-datasets">
        <animated.div id="no-datasets-wrapper" style={noDatasetsCardAnimations}>
          <Card id="no-datasets">
            <FontAwesomeIcon className="card-icon" icon={faFrown} size="6x" />
            <Text className="card-msg">Looks like you don't have any datasets yet</Text>
            <Button
              className="card-btn"
              fill={true}
              minimal={true}
              text="Add Dataset"
              onClick={() => toggleShowNavbarAddBtn()} />
          </Card>
        </animated.div>
        <animated.div id="add-dataset-wrapper" style={addDatasetCardAnimations}>
          <Card id="add-dataset-card">
            <DatasetForm token={props.authService.token} />
          </Card>
        </animated.div>
      </div>
    </div>
  );
}

export default Home;