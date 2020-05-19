import React, { Component } from 'react'
import { Button, FormGroup, InputGroup } from "@blueprintjs/core"

class RegisterForm extends Component {
  constructor(props) {
    super(props)

    this.state = {
      username: '',
      password: '',
      email: '',
      firstName: '',
      lastName: '',
      registered: false,
      error: undefined
    }

    this.handleUsernameChange = this.handleUsernameChange.bind(this)
    this.handlePasswordChange = this.handlePasswordChange.bind(this)
    this.handleEmailChange = this.handleEmailChange.bind(this)
    this.handleFirstNameChange = this.handleFirstNameChange.bind(this)
    this.handleLastNameChange = this.handleLastNameChange.bind(this)
    this.handleSubmit = this.handleSubmit.bind(this)
  }

  handleUsernameChange(event) {
    this.setState({username: event.target.value})
  }

  handlePasswordChange(event) {
    this.setState({password: event.target.value})
  }

  handleEmailChange(event) {
    this.setState({email: event.target.value})
  }

  handleFirstNameChange(event) {
    this.setState({firstName: event.target.value})
  }

  handleLastNameChange(event) {
    this.setState({lastName: event.target.value})
  }

  handleSubmit() {
    fetch('/users/register/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: this.state.username,
        password: this.state.password,
        email: this.state.email,
        first_name: this.state.firstName,
        last_name: this.state.lastName
      })
    })
    .then(res => res.json())
    .then(
      (result) => {
        this.setState({
          registered: true
        })

        this.props.loginHandler(this.state.username)
      },
      (error) => {
        this.setState({
          error: error
        })
      }
    )
  }

  render() {
    return (
      <div>
        <h1>Login</h1>
        <p>Already have an account? 
          <a href="#" onClick={this.props.toggleLogin}> Log in.</a>
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

        <FormGroup
          label="Email"
          labelFor="email-input">      
          <InputGroup
            id="email-input"
            placeholder="your@email.com"
            type="email"
            value={this.state.email}
            onChange={this.handleEmailChange} />
        </FormGroup>

        <FormGroup
          label="First Name"
          labelFor="first-name-input">      
          <InputGroup
            id="first-name-input"
            placeholder="Enter your first name"
            type="text"
            value={this.state.firstName}
            onChange={this.handleFirstNameChange} />
        </FormGroup>

        <FormGroup
          label="Last Name"
          labelFor="last-name-input">      
          <InputGroup
            id="last-name-input"
            placeholder="Enter your last name"
            type="text"
            value={this.state.lastName}
            onChange={this.handleLastNameChange} />
        </FormGroup>

        <Button
          id="submit-btn"
          large={true}
          minimal={true}
          outlined={true}
          type="submit" 
          onClick={this.handleSubmit}>
            Register
        </Button>
      </div>
    )
  }
}

export default RegisterForm