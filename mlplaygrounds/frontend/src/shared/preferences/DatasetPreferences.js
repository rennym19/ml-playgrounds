class DatasetPreferences {
 
  static get STORAGE() { return window.localStorage }

  static get SELECTED_DATASET_STORAGE_ITEM() { return 'selected_dataset' }

  static saveSelectedDataset(dataset) {
    if (dataset !== undefined) {
      DatasetPreferences.STORAGE.setItem(
        DatasetPreferences.SELECTED_DATASET_STORAGE_ITEM,
        JSON.stringify({uid: dataset.uid, name: dataset.name})
      );
    }
  }

  static retrieveSelectedDataset() {
    let dataset = DatasetPreferences.STORAGE.getItem(DatasetPreferences.SELECTED_DATASET_STORAGE_ITEM);
    if (dataset !== null) {
      return JSON.parse(dataset);
    }
    return undefined;
  }
}

export default DatasetPreferences;