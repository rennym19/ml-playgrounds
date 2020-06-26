import React from 'react';
import { Dialog, Classes } from '@blueprintjs/core';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes } from '@fortawesome/free-solid-svg-icons';

import ModelForm from '../Forms/ModelForm';
import './ModelDialog.css';

const ModelDialog = (props) => {
  return (
    <Dialog isOpen={props.isOpened} onClose={props.toggleOpened} className="model-form-dialog">
      <div id="model-dialog-header" className={Classes.DIALOG_HEADER}>
        <h1 id="model-dialog-title">Create new Model</h1>
        <div id="model-dialog-close" className={Classes.DIALOG_CLOSE_BUTTON}>
          <span className="close-icon-wrapper" onClick={props.toggleOpened}>
            <FontAwesomeIcon
              icon={faTimes}
              size="lg"/>
          </span>
        </div>
      </div>
      <div className="model-form-dialog-body">
        <ModelForm
          authService={props.authService}
          datasetId={props.datasetId}
          features={props.features}
          problemType={props.problemType} />
      </div>
    </Dialog>
  );
};

export default ModelDialog;