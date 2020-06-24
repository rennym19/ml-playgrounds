import APIService from './APIService';
import { notify } from '../../notifications/Notifier';

class DatasetsAPIService extends APIService{
  static getDatasets(token, success, error=undefined) {
    this.list('data/datasets/', token, success, error);
  }

  static getDataset(uid, token, success, error=undefined) {
    this.get(`data/datasets/${uid}/`, token, success, error);
  }

  static addDataset(token, dataset, success=undefined, error=undefined) {
    const requestBody = DatasetsAPIService.buildMultipartData(dataset);

    const handleSuccess = (res) => {
      notify(
        'Congrats!',
        `The dataset "${dataset.name}" has been added succesfully.`,
        'success'
      );
      if (success !== undefined) { success(res); }
    }

    this.create('data/parse_dataset/', token, requestBody, false, handleSuccess, error );
  }

  static buildMultipartData(dataset) {
    const formData = new FormData();
    formData.append('name', dataset.name);
    formData.append('label', dataset.label);
    formData.append('problem_type', dataset.problemType);
    formData.append('data', dataset.data);
    return formData;
  }
}

export default DatasetsAPIService;