import React from 'react';

import NoDatasetsCard from './Cards/NoDatasetsCard';
import DatasetForm from './Forms/DatasetForm';

const NoDatasets = (props) => {
  return (
    <>
    {
      props.showNavbarAddBtn
        ? <NoDatasetsCard toggleShowNavbarAddBtn={props.toggleShowNavbarAddBtn} />
        : <DatasetForm
            token={props.authService.token}
            toggleShowNavbarAddBtn={props.toggleShowNavbarAddBtn} />
    }
    </>
  );
};

export default NoDatasets;