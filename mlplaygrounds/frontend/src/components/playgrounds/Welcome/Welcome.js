import React, { Component } from "react"

import AppInfo from '../Info/AppInfo'
import Auth from "../Auth/Auth"

import './Welcome.css'

class Welcome extends Component {
  constructor(props) {
    super(props)
  }

  render() {
    return (
      <div className="Container">
        <Auth authService={this.props.authService}></Auth>
        <AppInfo />
      </div>
    )
  }
}

export default Welcome