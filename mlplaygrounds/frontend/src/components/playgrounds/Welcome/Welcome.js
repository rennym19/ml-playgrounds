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
        <Auth loginHandler={this.props.loginHandler}></Auth>
        <AppInfo />
      </div>
    )
  }
}

export default Welcome