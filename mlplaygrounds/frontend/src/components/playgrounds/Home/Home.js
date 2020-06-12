import React, { useState, useEffect, useCallback } from 'react';
import { useSpring, animated } from 'react-spring';

import UsersAPIService from '../../../shared/data/api/Users';
import DatasetPreferences from '../../../shared/preferences/DatasetPreferences';
import NoDatasets from '../Datasets/NoDatasets';
import SelectDatasetCard from '../Datasets/Cards/SelectDatasetCard';
import Dataset from '../Datasets/Dataset';
import Nav from '../Nav/Nav';
import './Home.css';

const Home = (props) => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [registrationDate, setRegistrationDate] = useState('');
  const [datasets, setDatasets] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState(undefined);
  const [showNavbarAddBtn, setShowNavbarAddBtn] = useState(true);

  useEffect(() => {
    let retrievedDataset = DatasetPreferences.retrieveSelectedDataset();
    if (retrievedDataset !== undefined)
      setSelectedDataset(retrievedDataset);

    UsersAPIService.retrieveUserProfile(
      props.authService.token,
      res => {
        setUsername(res.username);
        setEmail(res.email);
        setFirstName(res.first_name);
        setLastName(res.last_name);
        setRegistrationDate(res.registration_date);
        setDatasets(res.datasets);
      },
      () => props.authService.authLogout()
    );
  }, []);

  useEffect(() => {
    DatasetPreferences.saveSelectedDataset(selectedDataset);
  }, [selectedDataset]);

  const toggleShowNavbarAddBtn = () => { setShowNavbarAddBtn(!showNavbarAddBtn); }

  return (
    <div id="Home">
      <Nav
        id="Navbar"
        showNavbarAddBtn={showNavbarAddBtn}
        authService={props.authService}
        addDataset={toggleShowNavbarAddBtn}
        datasets={datasets}
        selectedDataset={selectedDataset}
        setSelectedDataset={setSelectedDataset} />
      <div id="Content" className={selectedDataset === undefined ? "unselected-dataset" : ""}>
        {
          selectedDataset !== undefined && showNavbarAddBtn
            ? <Dataset
                authService={props.authService}
                selectedDataset={selectedDataset} />
            : <animated.div id="card-wrapper">
                {
                  datasets.length === 0 || !showNavbarAddBtn
                  ? <NoDatasets
                    authService={props.authService}
                    showNavbarAddBtn={showNavbarAddBtn}
                    toggleShowNavbarAddBtn={toggleShowNavbarAddBtn} />
                  : <SelectDatasetCard
                      authService={props.authService}
                      datasets={datasets}
                      setSelectedDataset={setSelectedDataset} />
                }
              </animated.div>
        }
      </div>
    </div>
  );
}

export default Home;