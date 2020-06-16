import React, { useState } from 'react'
import { Card, RadioGroup, Radio } from '@blueprintjs/core';
import { Button, FormGroup, InputGroup, FileInput } from '@blueprintjs/core'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes } from '@fortawesome/free-solid-svg-icons';

import DatasetValidator from '../../../../shared/validators/datasets';
import { notifyValidatorErrors } from '../../../../shared/notifications/Notifier';
import DatasetsAPIService from '../../../../shared/data/api/Datasets';
import './DatasetForm.css'

const getFileName = (fullPath) => {
  if (fullPath) {
    let startIndex = (fullPath.indexOf('\\') >= 0 ? fullPath.lastIndexOf('\\') : fullPath.lastIndexOf('/'));
    let filename = fullPath.substring(startIndex);
    if (filename.indexOf('\\') === 0 || filename.indexOf('/') === 0) {
        filename = filename.substring(1);
    }
    return filename;
  }
};

const DatasetForm = (props) => {
  const [name, setName] = useState('');
  const [data, setData] = useState(undefined);
  const [datasetFilename, setDatasetFilename] = useState(undefined);
  const [label, setLabel] = useState('');
  const [problemType, setProblemType] = useState(undefined);

  const onChangeName = e => setName(e.target.value);

  const onChangeDataFile = e => {
    setData(e.target.files[0]);
    setDatasetFilename(getFileName(e.target.value));
  };

  const onChangeLabel = e => setLabel(e.target.value);

  const onChangeProblemType = e => setProblemType(e.target.value);

  const validate = () => {
    const validator = new DatasetValidator({
      name: name,
      data: data,
      label: label,
      problemType: problemType
    });

    if (!validator.isValid()) {
      notifyValidatorErrors(validator.getErrors());
      return false;
    }
    return true;
  };

  const handleSubmit = () => {
    if (validate())
      DatasetsAPIService.addDataset(
        props.token,
        {
          name: name,
          label: label,
          problemType: problemType,
          data: data
        },
        clearState
      );
  };

  const clearState = () => {
    setName('');
    setData(undefined);
    setDatasetFilename(undefined);
    setLabel('');
    setProblemType(undefined);
  };

  return (
    <Card id="add-dataset-card">
      <div className="form-wrapper">
        <div id="form-header">
          <h1>Add Dataset</h1>
          <span id="close-button-wrapper">
            <FontAwesomeIcon
              id="close-button"
              icon={faTimes}
              size="lg"
              onClick={() => props.toggleShowNavbarAddBtn()}/>
          </span>
        </div>
        <FormGroup
          label="Dataset Name"
          labelFor="name-input">      
          <InputGroup
            id="name-input"
            placeholder="Enter dataset name"
            type="text"
            fill={true}
            value={name}
            onChange={onChangeName} />
        </FormGroup>
        <FormGroup
          label="Data File"
          labelFor="data-file-input">
          <FileInput
            id="data-file-input"
            fill={true}
            placeholder="Choose dataset file..."
            text={datasetFilename}
            onInputChange={onChangeDataFile} />
        </FormGroup>
        <FormGroup
          label="Label Name"
          labelFor="label-input">      
          <InputGroup
            id="label-input"
            placeholder="Enter label name"
            type="text"
            fill={true}
            value={label}
            onChange={onChangeLabel} />
        </FormGroup>
        <RadioGroup
          label="Problem Type"
          onChange={onChangeProblemType}
          selectedValue={problemType}
          inline={true}>
            <Radio label="Regression" value="regression" className="radio-item" />
            <Radio label="Classification" value="classification" className="radio-item" />
        </RadioGroup>
      </div>
      <Button
        id="submit-btn"
        minimal={true}
        outlined={true}
        fill={true}
        type="submit" 
        onClick={handleSubmit}
        text="Add" />
    </Card>
  )
};

export default DatasetForm;