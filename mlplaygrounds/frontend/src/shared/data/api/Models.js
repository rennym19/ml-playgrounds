import APIService from './APIService';
import { notify } from '../../notifications/Notifier';

class ModelsAPIService extends APIService {
  static getModels(token, datasetId=undefined, success=undefined, err=undefined) {
    let url = datasetId === undefined ? 'data/models/' : `data/models/?dataset_id=${datasetId}`
    this.list(url, token, success, err);
  }

  static addModel(token, model, success=undefined, err=undefined) {
    const handleSuccess = (res) => {
      notify(
        'Congrats!',
        `The model "${model.name}" has been added succesfully.`,
        'success'
      );
      if (success !== undefined) { success(res); }
    }

    this.create('data/models/', token, JSON.stringify(model), true, handleSuccess, err);
  }

  static getModel(token, uid, success=undefined, err=undefined) {
    this.get(`data/models/${uid}/`, token, success, err);
  }

  static patchModel(token, uid, model, success=undefined, err=undefined) {
    this.patch(`data/models/${uid}/`, token, JSON.stringify(model), true, success, err);
  }

  static deleteModel(token, uid, success=undefined, err=undefined) {
    this.delete(`data/models/${uid}/`, token, success, err);
  }
}

export default ModelsAPIService;