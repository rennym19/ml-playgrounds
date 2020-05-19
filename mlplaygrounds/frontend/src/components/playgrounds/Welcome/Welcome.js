import React, { Component } from "react"
import { render } from "react-dom"

import AppInfo from '../Info/AppInfo'
import Login from "../Login/Login"

import './Welcome.css'

class Welcome extends Component {
  constructor(props) {
    super(props)
    this.userLoggedIn = false
  }

  render() {
    return (
      <div className="Container">
        <Login userLoggedIn={this.userLoggedIn}></Login>
        <AppInfo />
      </div>
    )
  }
}

export default Welcome