import React, { Component } from 'react'
import { Button, FormGroup, InputGroup } from "@blueprintjs/core"

import { notifyErrors } from '../../../utils/Notifier'

class LoginForm extends Component {
  constructor(props) {
    super(props)

    this.state = {
      username: '',
      password: ''
    }

    this.handleUsernameChange = this.handleUsernameChange.bind(this)
    this.handlePasswordChange = this.handlePasswordChange.bind(this)
    this.handleSubmit = this.handleSubmit.bind(this)
  }

  handleUsernameChange(event) {
    this.setState({username: event.target.value})
  }

  handlePasswordChange(event) {
    this.setState({password: event.target.value})
  }

  handleSubmit(event) {
    fetch('/users/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: this.state.username,
        password: this.state.password,
      })
    })
    .then(res => res.json().then(data => ({status: res.status, body: data})))
    .then(result => {
      if (result.status === 200)
        this.props.loginHandler(result.body.user.username, result.body.token)
      else
        notifyErrors(result.body)
    })
  }

  render() {
    return (
      <div>
        <h1>Login</h1>
        <p>Don't have an account?
          <a href="#" onClick={this.props.toggleLogin}> Create your account.</a>
        </p>
        <FormGroup
          label="Username"
          labelFor="username-input">      
          <InputGroup
            id="username-input"
            placeholder="Enter username"
            type="text"
            value={this.state.username}
            onChange={this.handleUsernameChange} />
        </FormGroup>
        <FormGroup
          label="Password"
          labelFor="password-input">

          <InputGroup
            id="password-input"
            placeholder="Enter password"
            type="password"
            value={this.state.password}
            onChange={this.handlePasswordChange} />
        </FormGroup>
        <a id="forgot-password-btn" href="#">Forgot password?</a>
        <Button
          id="submit-btn"
          large={true}
          minimal={true}
          outlined={true}
          type="submit" 
          onClick={this.handleSubmit}>
            Login
        </Button>
      </div>
    )
  }
}

export default LoginForm
