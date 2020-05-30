import React, { Component } from 'react'
import { Button, FormGroup, InputGroup, FileInput } from '@blueprintjs/core'

import { notifyErrors } from '../../../../utils/Notifier'
import './DatasetForm.css'

class DatasetForm extends Component {
  constructor(props) {
    super(props)

    this.state = {
      'name': '',
      'data': undefined
    }

    this.onChangeName = this.onChangeName.bind(this)
    this.onChangeDataFile = this.onChangeDataFile.bind(this)
  }

  onChangeName(event) {
    this.setState({'name': event.target.value})
  }

  onChangeDataFile(event) {
    this.setState({'data': event.target.files[0]})
  }

  handleSubmit() {
    console.log('hello')
  }

  render() {
    return (
      <div id="add-dataset-form">
        <div class="form-wrapper">
          <h1>Add Dataset</h1>
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
              text="Choose dataset file..."
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
      </div>
    )
  }
}

export default DatasetForm