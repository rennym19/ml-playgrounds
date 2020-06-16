import { notify, notifyErrors } from '../../notifications/Notifier'

class UsersAPIService {  
  static registerUser(user, success) {
    fetch('users/register/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: user.username,
        password: user.password,
      })
    })
    .then(res => res.json().then(data => ({status: res.status, body: data})))
    .then(result => {
      if (result.status === 200)
        success(result);
      else
        notifyErrors(result.body);
    });
  }
  
  static loginUser(user, success) {
    fetch('users/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: user.username,
        password: user.password,
      })
    })
    .then(res => res.json().then(data => ({status: res.status, body: data})))
    .then(result => {
      if (result.status === 200)
        success(result);
      else
        notifyErrors(result.body);
    });
  }
  
  static logoutUser(token, success) {
    if (token === undefined)
      notify('Error', 'Were you logged in?', 'danger');

    fetch('users/logout/', {
      method: 'POST',
      headers: { 'Authorization': `Token ${token}` }
    })
    .then(res => {
      if (res.status == 204) {
        success();
      } else {
        console.log('Error while logging out... Were you logged in?');
      }
    });
  }

  static retrieveUserProfile(token, success, logoutHandler) {
    fetch('users/profile/', {
      headers: { 'Authorization': `Token ${token}` }
    })
    .then(res => res.json().then(data => ({status: res.status, body: data})))
    .then(
      result => {
        if (result.status === 200) {
          success(result.body);
        } else {
          logoutHandler();
        }
      }
    );
  }
}

export default UsersAPIService;