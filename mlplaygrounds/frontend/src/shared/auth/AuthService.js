import UsersAPIService from '../data/api/Users'

class AuthService {
  constructor(client) {
    this.token = undefined;
    this.username = undefined;

    this.client = client;

    this.storage = window.localStorage;
  }

  static get AUTH_STORAGE_ITEM() { return 'auth' }

  register(data, loggedIn=undefined) {
    UsersAPIService.registerUser(data, result => {
      this.authLogin(this.getCredentialsFromResponseBody(result));
      
      if (loggedIn !== undefined)
        loggedIn();
    });
  }

  login(data, loggedIn=undefined) {
    UsersAPIService.loginUser(data, result => {
      this.authLogin(this.getCredentialsFromResponseBody(result));

      if (loggedIn !== undefined)
        loggedIn();
    })
  }

  logout(loggedOut=undefined) {
    UsersAPIService.logoutUser(this.token, () => {
      this.authLogout();

      if (loggedOut !== undefined)
        loggedOut();
    });
  }

  isLoggedIn() {
    return this.token !== undefined && this.username !== undefined ? true : false;
  }

  getCredentialsFromResponseBody(response) {
    return {
      username: response.body.user.username,
      token: response.body.token
    }
  }

  authLogin(user, saveInStorage=true) {
    this.username = user.username;
    this.token = user.token;

    this.client.setLoggedIn(true);

    if (saveInStorage)
      this.saveAuthInStorage(user);
  }

  authLogout() {
    this.username = undefined;
    this.token = undefined;

    this.client.setLoggedIn(false);

    this.clearAuthStorage();
  }

  retrieveAuthFromStorage() {
    let auth = this.storage.getItem(AuthService.AUTH_STORAGE_ITEM);
    if (auth !== null) {
      auth = JSON.parse(auth);
      this.authLogin({username: auth.username, token: auth.token}, false);
    }
  }

  saveAuthInStorage(user) {
    this.storage.setItem(
      AuthService.AUTH_STORAGE_ITEM,
      JSON.stringify({username: user.username, token: user.token})
    );
  }

  clearAuthStorage() {
    this.storage.clear();
  }
}

export default AuthService;