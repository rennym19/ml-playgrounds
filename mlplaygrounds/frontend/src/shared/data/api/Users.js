import APIService from './APIService';
import { notify, notifyErrors } from '../../notifications/Notifier'

class UsersAPIService extends APIService {
  static registerUser(user, success) {
    this.create('users/register/', null, JSON.stringify(user), true, success);
  }
  
  static loginUser(user, success) {
    this.post('users/login/', null, JSON.stringify(user), true, 200, success);
  }
  
  static logoutUser(token, success) {
    if (token === undefined)
      notify('Error', 'Were you logged in?', 'danger');
    else
      this.post('users/logout/', token, undefined, false, 204, success);
  }

  static retrieveUserProfile(token, success, logoutHandler) {
    this.get('users/profile/', token, success, logoutHandler);
  }
}

export default UsersAPIService;