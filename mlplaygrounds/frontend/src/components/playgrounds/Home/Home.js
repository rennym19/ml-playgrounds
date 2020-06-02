import React, { useState, useEffect, useCallback } from 'react';
import { useSpring, animated } from 'react-spring';

import UsersAPIService from '../../../shared/data/api/Users';
import DatasetForm from '../Datasets/Forms/DatasetForm';
import NoDatasets from '../Datasets/Info/NoDatasets';
import Nav from '../Nav/Nav';
import './Home.css';

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
        setLastName(res.last_name)
        setRegistrationDate(res.registration_date)
      },
      props.authService.authLogout
    );
  }, []);

  const toggleShowNavbarAddBtn = () => { setShowNavbarAddBtn(!showNavbarAddBtn); }

  return (
    <div id="Home">
      <Nav
        id="Navbar"
        showNavbarAddBtn={showNavbarAddBtn}
        username={username}
        authService={props.authService}
        addDataset={toggleShowNavbarAddBtn} />
      <div id="Content" className="no-datasets">
        <animated.div id="card-wrapper">
          { 
            showNavbarAddBtn
              ? <NoDatasets toggleShowNavbarAddBtn={toggleShowNavbarAddBtn} />
              : <DatasetForm
                  token={props.authService.token}
                  toggleShowNavbarAddBtn={toggleShowNavbarAddBtn} />
          }
        </animated.div>
      </div>
    </div>
  );
}

export default Home;