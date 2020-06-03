class DatasetValidator {
  constructor(dataset) {
    this.dataset = dataset;
    this.errors = [];
  }

  isValid() {
    return this.validateName() && this.validateData();
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

    // Check if name already in use

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