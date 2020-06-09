import React from 'react';
import { Button, MenuItem } from '@blueprintjs/core';
import { Select } from '@blueprintjs/select';

const SelectColumnForm = (props) => {
  const renderColumn = (column, { handleClick }) => {
    return (
      <MenuItem 
        key={column}
        label={column}
        text={column}
        onClick={handleClick} />
    );
  };

  return (
    <Select
      id={props.id}
      items={props.columns}
      filterable={false}
      itemRenderer={renderColumn}
      onItemSelect={props.handleColumnSelect} >
        <Button
          minimal={true}
          text={props.column === undefined ? 'Select a Column' : props.column}
          rightIcon="caret-down" />
    </Select>
  );
};

export default SelectColumnForm;