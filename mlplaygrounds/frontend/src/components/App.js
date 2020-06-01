import React, { Component } from 'react'
import { render } from 'react-dom'
import ReactNotification from 'react-notifications-component'

import Home from './playgrounds/Home/Home'
import Welcome from './playgrounds/Welcome/Welcome'

import AuthService from '../shared/auth/AuthService';
import './App.css'

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      authService: new AuthService(this),
      loggedIn: false
    };

    this.setLoggedIn = this.setLoggedIn.bind(this);
  }

  componentDidMount() {
    this.state.authService.retrieveAuthFromStorage();
  }

  setLoggedIn(loggedIn) {
    this.setState({
      loggedIn: loggedIn
    });
  }

  render() {
    let landingPage;
    if (this.state.loggedIn)
      landingPage = <Home authService={this.state.authService} />
    else
      landingPage = <Welcome authService={this.state.authService} />

    return (
      <div className='appContainer'>
        <ReactNotification />
        { landingPage }
      </div>
    )
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);
