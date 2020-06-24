import { notifyErrors } from '../../notifications/Notifier';

class APIService {
  static list(url, token, success=undefined, err=undefined) {
    this.makeRequest(
      { url: url, method: 'GET', token: token },
      { successCode: 200, success: success, err: err }
    );
  }

  static create(url, token, body, json=false, success=undefined, err=undefined) {
    this.makeRequest(
      { url: url, method: 'POST', token: token, body: body, json: json },
      { successCode: 201, success: success, err: err }
    );
  }

  static post(url, token, body, json=false, successCode=200, success=undefined, err=undefined) {
    this.makeRequest(
      { url: url, method: 'POST', token: token, body: body, json: json },
      { successCode, success, err }
    );
  }

  static get(url, token, success=undefined, err=undefined) {
    this.makeRequest(
      { url: url, method: 'GET', token: token },
      { successCode: 200, success: success, err: err }
    );
  }

  static patch(url, token, body, json=false, success=undefined, err=undefined) {
    this.makeRequest(
      { url: url, method: 'PATCH', token: token, body: body, json: json },
      { successCode: 200, success: success, err: err }
    );
  }

  static delete(url, token, success=undefined, err=undefined) {
    this.makeRequest(
      { url: url, method: 'DELETE', token: token },
      { successCode: 204, success: success, err: err }
    );
  }

  static makeRequest(requestOptions, responseOptions) {
    let { url, method, token, body, json } = requestOptions;
    let { successCode, success, err } = responseOptions;

    this.fetchUrl(url, method, token, body, json)
    .then(res => this.parseResponse(res))
    .then(parsedRes => this.handleParsedResponse(parsedRes, successCode, success, err));
  }

  static fetchUrl(url, method, token, body, json=false) {
    const headers = {};
    if (token !== null) { headers['Authorization'] = `Token ${token}`; }
    if (json) { headers['Content-Type'] = 'application/json'; }

    const requestOptions = {
      method: method,
      headers: headers
    };

    if (body !== undefined) { requestOptions['body'] = body; }
    
    return fetch(url, requestOptions);
  }

  static parseResponse(res) {
    if (res.status !== 204)
      return res.json().then(data => ({status: res.status, body: data}));

    return new Promise((resolve, reject) => {
      resolve({status: res.status});
    });
  }

  static handleParsedResponse(response, successCode,
                              success=undefined, err=undefined) {
    if (response.status === successCode) {
      if (success !== undefined) {
        if (response.hasOwnProperty('body'))
          success(response.body);
        else
          success();
      }
    } else {
      notifyErrors(response.body);

      if (err !== undefined) { err(response.body); }
    }
  }
}

export default APIService;