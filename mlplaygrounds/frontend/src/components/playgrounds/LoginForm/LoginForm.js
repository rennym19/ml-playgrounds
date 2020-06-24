import React, { useState } from 'react'
import { Button, FormGroup, InputGroup } from "@blueprintjs/core"

const LoginForm = (props) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleUsernameChange = e => setUsername(e.target.value);
  const handlePasswordChange = e => setPassword(e.target.value);

  const handleSubmit = e => props.authService.login({ username, password });

  return (
    <div>
      <h1>Login</h1>
      <p>Don't have an account?
        <a href="#" onClick={props.toggleLogin}> Create your account.</a>
      </p>
      <FormGroup
        label="Username"
        labelFor="username-input">      
        <InputGroup
          id="username-input"
          placeholder="Enter username"
          type="text"
          value={username}
          onChange={handleUsernameChange} />
      </FormGroup>
      <FormGroup
        label="Password"
        labelFor="password-input">

        <InputGroup
          id="password-input"
          placeholder="Enter password"
          type="password"
          value={password}
          onChange={handlePasswordChange} />
      </FormGroup>
      <a id="forgot-password-btn" href="#">Forgot password?</a>
      <Button
        id="submit-btn"
        large={true}
        minimal={true}
        outlined={true}
        type="submit" 
        onClick={handleSubmit}>
          Login
      </Button>
    </div>
  );
};

export default LoginForm
