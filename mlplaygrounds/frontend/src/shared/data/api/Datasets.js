import { notify, notifyErrors } from '../../notifications/Notifier';

class DatasetsAPIService {
  static getDatasets(token, success, error=undefined) {
    fetch('data/datasets/', {
      method: 'GET',
      headers: { 'Authorization': `Token ${token}` }
    })
    .then(res => res.json().then(data => ({status: res.status, body: data})))
    .then(result => {
      if (result.status === 200) {
        success(result.body);
      } else {
        notifyErrors(result.body);

        if (error !== undefined)
          error();
      }
    });
  }

  static getDataset(uid, token, success, error=undefined) {
    fetch(`data/datasets/${uid}/`, {
      method: 'GET',
      headers: { 'Authorization': `Token ${token}`}
    })
    .then(res => res.json().then(data => ({status: res.status, body: data})))
    .then(result => {
      if (result.status === 200) {
        success(result.body);
      } else {
        notifyErrors(result.body);

        if (error !== undefined)
          error();
      }
    });
  }

  static addDataset(token, dataset, success=undefined, error=undefined) {
    fetch('data/parse_dataset/', {
      method: 'POST',
      body: DatasetsAPIService.buildMultipartData(dataset),
      headers: { 'Authorization': `Token ${token}` }
    })
    .then(res => res.json().then(data => ({status: res.status, body: data})))
    .then(result => {
      if (result.status === 201) {
        notify('Congrats!',
               `The dataset "${dataset.name}" has been added succesfully.`,
               'success');
        
        if (success !== undefined)
          success();
      } else {
        notifyErrors(result.body);

        if (error !== undefined)
          error();
      }
    });
  }

  static buildMultipartData(dataset) {
    const formData = new FormData();
    formData.append('name', dataset.name);
    formData.append('label', dataset.label)
    formData.append('data', dataset.data);
    return formData;
  }
}

export default DatasetsAPIService;