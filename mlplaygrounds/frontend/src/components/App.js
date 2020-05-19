import React, { Component } from 'react'
import { render } from 'react-dom'
import Cookie from 'js-cookie'

import Home from './playgrounds/Home/Home'
import Welcome from './playgrounds/Welcome/Welcome'

import './App.css'

class App extends Component {
  constructor(props) {
    super(props)

    this.state = {
      userLoggedIn: false,
      username: undefined,
      activeSession: Cookie.get('sessionid')
    }

    this.loginUser = this.loginUser.bind(this)
    this.logoutUser = this.logoutUser.bind(this)
  }

  loginUser(username) {
    this.setState({
      username: username,
      userLoggedIn: true,
      activeSession: Cookie.get('sessionid')
    })
  }

  logoutUser() {
    this.setState({
      userLoggedIn: false,
      username: undefined,
      activeSession: undefined
    })
  }

  render() {
    return (
      <div>
      {this.state.activeSession
        ? <Home loginHandler={this.loginUser} logoutHandler={this.logoutUser} />
        : <Welcome loginHandler={this.loginUser} />
      }
      </div>
    )
  }
}

export default App

const container = document.getElementById("app")
render(<App />, container)
