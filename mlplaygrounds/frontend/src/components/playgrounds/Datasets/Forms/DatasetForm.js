import React, { Component } from 'react'
import { Card } from '@blueprintjs/core';
import { Button, FormGroup, InputGroup, FileInput } from '@blueprintjs/core'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes } from '@fortawesome/free-solid-svg-icons';

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
      'data': {},
      'datasetFileName': undefined
    }

    this.onChangeName = this.onChangeName.bind(this)
    this.onChangeDataFile = this.onChangeDataFile.bind(this)
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

  handleSubmit() {
    let formData = new FormData()
    formData.append('name', this.state.name)
    formData.append('data', this.state.data)

    fetch('data/parse_dataset/', {
      method: 'POST',
      body: formData,
      headers: {
        'Authorization': `Token ${this.props.token}`
      }
    })
    .then(res => {
      if (res.status == 201) {
        console.log('created')
      } else {
        console.log('error')
      }
    })
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