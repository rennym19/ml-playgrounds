import React, { Component } from 'react'
import { Button, FormGroup, InputGroup, Card, Elevation } from "@blueprintjs/core"

import LoginForm from '../LoginForm/LoginForm'
import RegisterForm from '../RegisterForm/RegisterForm'
import './Auth.css'


class Auth extends Component {
  constructor(props) {
    super(props)

    this.state = {
      login: true
    }

    this.toggleLogin = this.toggleLogin.bind(this)
  }

  toggleLogin() {
    this.setState({
      login: !this.state.login
    })
  }

  render() {
    let authForm;
    if (this.state.login) {
      authForm = <LoginForm 
                    toggleLogin={this.toggleLogin}
                    authService={this.props.authService} />
    } else {
      authForm = <RegisterForm
                    toggleLogin={this.toggleLogin}
                    authService={this.props.authService} />
    }

    return (
      <div className="Auth">
        <Card elevation={Elevation.TWO}>
          { authForm }
        </Card>
      </div>
    )
  }
}

export default Auth