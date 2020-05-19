import React from 'react';
import { Button, FormGroup, InputGroup, Card, Elevation } from "@blueprintjs/core";

import './Login.css'

function Login(props) {
  return (
    <div className="Login">
      <Card elevation={Elevation.TWO}>
        <h1>Login</h1>
        <p>Don't have an account? <a href="#">Create your account.</a></p>
        <FormGroup
          label="Username"
          labelFor="username-input">
            
          <InputGroup id="username-input"
                      placeholder="Enter username"
                      type="text" />
        </FormGroup>
        <FormGroup
          label="Password"
          labelFor="password-input">

          <InputGroup id="password-input"
                      placeholder="Enter password"
                      type="password" />
        </FormGroup>
        <a id="forgot-password-btn" href="#">Forgot password?</a>
        <Button id="login-submit-btn"
                large={true}
                minimal={true}
                outlined={true}
                type="submit" >
          Login
        </Button>
      </Card>
    </div>
  )
}

export default Login