import React, { useState, useEffect } from 'react';
import { Button, MenuItem, FormGroup, InputGroup } from '@blueprintjs/core';
import { Select, MultiSelect } from '@blueprintjs/select';

import ModelsAPIService from '../../../../shared/data/api/Models';
import './ModelForm.css';

const ModelForm = (props) => {
  const [name, setName] = useState('');
  const [algorithm, setAlgorithm] = useState(undefined);
  const [selectedFeatures, setSelectedFeatures] = useState([]);

  let algorithms = [];
  if (props.problemType === 'regression') {
    algorithms = [
      {name: 'Linear Regression', val: 'linear'},
      {name: 'Decission Tree', val: 'decisiontree'}
    ];
  } else if (props.problemType === 'classification') {
    algorithms = [
      {name: 'Logistic Regression', val: 'logistic'},
      {name: 'Support Vector Machines', val: 'svm'}
    ];
  }

  const onChangeName = e => setName(e.target.value);
  const onChangeAlgorithm = (algorithm, e) => setAlgorithm(algorithm);

  let clearButton;

  useEffect(() => {
    updateClearButton()
  }, [selectedFeatures]);

  const updateClearButton = () => {
    if (selectedFeatures.length > 0) {
      clearButton = <Button icon="cross" minimal={true} onClick={handleClear}/>;
    } else {
      clearButton = null;
    }
  };

  const renderAlgorithm = (algorithm, { handleClick }) => {
    return (
      <MenuItem 
        key={algorithm.val}
        label={algorithm.name}
        text={algorithm.name}
        onClick={handleClick} />
    );
  };

  const renderFeature = (feature, { modifiers, handleClick }) => {
    return (
      <MenuItem
        active={modifiers.active}
        icon={isFeatureSelected(feature) ? "tick" : "blank"}
        key={feature}
        text={feature}
        onClick={handleClick} />
    )
  };

  const getSelectedFeatureIndex = (feature) => {
    return selectedFeatures.indexOf(feature);
  }

  const isFeatureSelected = (feature) => {
    return selectedFeatures.indexOf(feature) !== -1
  };

  const selectFeature = (feature) => {
    setSelectedFeatures([...selectedFeatures, feature]);
  };

  const deselectFeature = (index) => {
    let newSelectedFeatures = [...selectedFeatures];
    newSelectedFeatures.splice(index, 1);
    setSelectedFeatures(newSelectedFeatures);
  };

  const handleFeatureSelect = (feature) => {
    if (!isFeatureSelected(feature)) {
      selectFeature(feature);
    } else {
      deselectFeature(getSelectedFeatureIndex(feature));
    }
    
    console.log(selectedFeatures);
  };
  
  const handleTagRemove = (tag, index) => {
    deselectFeature(index);
  };

  const handleClear = () => setSelectedFeatures([]);

  const handleSubmit = () => {
    ModelsAPIService.addModel(
      props.authService.token,
      {
        name: name,
        algorithm: algorithm.val,
        features: selectedFeatures,
        dataset_id: props.datasetId,
      }
    );
  };

  return (
    <div>
      <div id="model-form-wrapper">
        <FormGroup
          label="Model Name"
          labelFor="model-name">
          <InputGroup
            id="model-name"
            placeholder="Enter model name"
            type="text"
            fill={true}
            value={name}
            minLength={1}
            required={true}
            onChange={onChangeName} />
        </FormGroup>
        <FormGroup
          label="Algorithm"
          className="select-wrapper">
          <Select
            fill={true}
            items={algorithms}
            filterable={false}
            itemRenderer={renderAlgorithm}
            onItemSelect={onChangeAlgorithm}>
              <Button
                fill={true}
                minimal={true}
                text={algorithm === undefined ? 'Select a ML Algorithm' : algorithm.name}
                rightIcon="caret-down" />
          </Select>
        </FormGroup>
        <FormGroup
          label="Features to exclude">
          <MultiSelect
            id="select-features"
            fill={true}
            items={props.features}
            itemRenderer={renderFeature}
            tagRenderer={feature => feature}
            onItemSelect={handleFeatureSelect}
            tagInputProps={{onRemove: handleTagRemove, rightElement: clearButton}}
            selectedItems={selectedFeatures}>
          </MultiSelect>
        </FormGroup>
      </div>
      <Button
        id="submit-model-btn"
        minimal={true}
        outlined={true}
        fill={true}
        type="submit"
        text="Create"
        onClick={handleSubmit} />
    </div>
  );
};

export default ModelForm;