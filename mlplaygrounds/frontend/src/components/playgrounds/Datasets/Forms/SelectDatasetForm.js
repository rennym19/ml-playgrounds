import React from 'react';
import { Button, MenuItem } from '@blueprintjs/core';
import { Select } from '@blueprintjs/select';

const SelectDatasetForm = (props) => {
  const renderDataset = (dataset, { handleClick }) => {
    return (
      <MenuItem 
        key={dataset.uid}
        label={dataset.name}
        text={dataset.name}
        onClick={handleClick} />
    );
  };

  return (
    <Select
      items={props.datasets}
      filterable={false}
      itemRenderer={renderDataset}
      onItemSelect={props.handleItemSelect} >
        <Button
          minimal={true}
          text={props.dataset === undefined ? 'Select a Dataset' : props.dataset.name}
          rightIcon="caret-down" />
    </Select>
  );
};

export default SelectDatasetForm;