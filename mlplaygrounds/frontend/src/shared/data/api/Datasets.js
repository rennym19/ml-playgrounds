import { notify, notifyErrors } from '../../notifications/Notifier';

class DatasetsAPIService {
  static addDataset(token, dataset, success=undefined, error=undefined) {
    fetch('data/parse_dataset/', {
      method: 'POST',
      body: DatasetsAPIService.buildMultipartData(dataset),
      headers: { 'Authorization': `Token ${token}` }
    })
    .then(res => res.json().then(data => ({status: res.status, body: data})))
    .then(result => {
      if (result.status == 201) {
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
    formData.append('data', dataset.data);
    return formData;
  }
}

export default DatasetsAPIService;