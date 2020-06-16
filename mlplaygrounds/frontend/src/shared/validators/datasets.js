class DatasetValidator {
  constructor(dataset) {
    this.dataset = dataset;
    this.errors = [];
  }

  isValid() {
    return this.validateName() && this.validateData() && this.validateLabel() && this.validateProblemType();
  }

  validateName() {
    this.errors.splice(this.errors.findIndex(err => err.field === 'name'));

    if (this.dataset.name === undefined || this.dataset.name.length === 0) {
      this.errors.push({
        field: 'name',
        errors: ['Dataset\'s name must be at least one character(s) long.']
      });
      return false;
    }

    return true;
  }

  validateLabel() {
    this.errors.splice(this.errors.findIndex(err => err.field === 'label'));

    if (this.dataset.label === undefined || this.dataset.label.length === 0) {
      this.errors.push({
        field: 'label',
        errors: ['You must enter a label name.']
      });
      return false;
    }

    return true;
  }

  validateProblemType() {
    this.errors.splice(this.errors.findIndex(err => err.field === 'problem type'));

    if (this.dataset.problemType === undefined) {
      this.errors.push({
        field: 'problem type',
        errors: ['You must tell us wheter this is a regression or a classification problem.']
      });
      return false;
    } else if (this.dataset.problemType !== 'classification' &&
               this.dataset.problemType  !== 'regression') {
      this.errors.push({
        field: 'problem type',
        errors: ['Only "classification" or "regression" are allowed.']
      });
      return false;
    }

    return true;
  }

  validateData() {
    this.errors.splice(this.errors.findIndex(err => err.field === 'data'));

    if (this.dataset.data === undefined) {
      this.errors.push({
        field: 'data',
        errors: ['You must choose your dataset\'s file.']
      });
      return false;
    }

    return true;
  }

  getErrors() {
    return this.errors;
  }
}

export default DatasetValidator;