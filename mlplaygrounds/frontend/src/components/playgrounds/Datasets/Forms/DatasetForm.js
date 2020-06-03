import React, { Component } from 'react'
import { Card } from '@blueprintjs/core';
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

class DatasetForm extends Component {
  constructor(props) {
    super(props)

    this.state = {
      'name': '',
      'data': undefined,
      'datasetFileName': undefined
    }

    this.onChangeName = this.onChangeName.bind(this)
    this.onChangeDataFile = this.onChangeDataFile.bind(this)
    this.validate = this.validate.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this)
  }

  onChangeName(event) {
    this.setState({'name': event.target.value})
  }

  onChangeDataFile(event) {
    this.setState({
      'data': event.target.files[0],
      'datasetFileName': getFileName(event.target.value)
    });
  }

  validate() {
    const validator = new DatasetValidator({
      name: this.state.name,
      data: this.state.data
    });

    if (!validator.isValid()) {
      notifyValidatorErrors(validator.getErrors());
      return false;
    }
    return true;
  }

  handleSubmit() {
    if (this.validate())
      DatasetsAPIService.addDataset(
        this.props.token,
        { name: this.state.name, data: this.state.data },
        () => {
          this.setState({
            'name': '',
            'data': undefined,
            'datasetFileName': undefined
          });
        }
      );
  }

  render() {
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
                onClick={() => this.props.toggleShowNavbarAddBtn()}/>
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
              value={this.state.name}
              onChange={this.onChangeName} />
          </FormGroup>
          <FormGroup
            label="Data File"
            labelFor="data-file-input">

            <FileInput
              id="data-file-input"
              fill={true}
              placeholder="Choose dataset file..."
              text={this.state.datasetFileName}
              onInputChange={this.onChangeDataFile} />
          </FormGroup>
        </div>
        <Button
          id="submit-btn"
          minimal={true}
          outlined={true}
          fill={true}
          type="submit" 
          onClick={this.handleSubmit}
          text="Add" />
      </Card>
    )
  }
}

export default DatasetForm