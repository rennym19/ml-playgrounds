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
      token: undefined 
    }

    this.storage = window.localStorage

    this.loginUser = this.loginUser.bind(this)
    this.logoutUser = this.logoutUser.bind(this)
    this.getAuthFromStorage = this.getAuthFromStorage.bind(this)
    this.saveAuthInStorage = this.saveAuthInStorage.bind(this)
    this.clearAuthStorage = this.clearAuthStorage.bind(this)
  }

  componentDidMount() {
    this.getAuthFromStorage()
  }

  static get AUTH_STORAGE_ITEM() { return 'auth' }

  loginUser(username, token, saveInStorage=true) {
    this.setState({
      username: username,
      userLoggedIn: true,
      token: token
    })

    if (saveInStorage) {
      this.saveAuthInStorage(username, token)
    }
  }

  logoutUser() {
    this.setState({
      userLoggedIn: false,
      username: undefined,
      token: undefined
    })

    this.clearAuthStorage()
  }

  getAuthFromStorage() {
    let auth = this.storage.getItem(App.AUTH_STORAGE_ITEM)
    if (auth !== null) {
      auth = JSON.parse(auth)
      this.loginUser(auth.username, auth.token, false)
    }
  }

  saveAuthInStorage(username, token) {
    this.storage.setItem(
      App.AUTH_STORAGE_ITEM,
      JSON.stringify({username: username, token: token})
    )
  }

  clearAuthStorage() {
    this.storage.removeItem('auth')
  }

  render() {
    if (this.state.userLoggedIn) {
      return <Home token={this.state.token} logoutHandler={this.logoutUser} />
    }
    return <Welcome loginHandler={this.loginUser} />
  }
}

export default App

const container = document.getElementById("app")
render(<App />, container)
