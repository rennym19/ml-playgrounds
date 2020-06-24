import React, { useState } from 'react'
import { Button, FormGroup, InputGroup } from "@blueprintjs/core"

const RegisterForm = (props) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');

  const handleUsernameChange = (e) => setUsername(e.target.value);
  const handlePasswordChange = (e) => setPassword(e.target.value);
  const handleEmailChange = (e) => setEmail(e.target.value);
  const handleFirstNameChange = (e) => setFirstName(e.target.value);
  const handleLastNameChange = (e) => setLastName(e.target.value);

  const handleSubmit = () => {
    props.authService.register({
      username: username,
      password: password,
      email: email,
      first_name: firstName,
      last_name: lastName
    });
  };

  return (
    <div>
      <h1>Register</h1>
      <p>Already have an account? 
        <a href="#" onClick={props.toggleLogin}> Log in.</a>
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

      <FormGroup
        label="Email"
        labelFor="email-input">      
        <InputGroup
          id="email-input"
          placeholder="your@email.com"
          type="email"
          value={email}
          onChange={handleEmailChange} />
      </FormGroup>

      <FormGroup
        label="First Name"
        labelFor="first-name-input">      
        <InputGroup
          id="first-name-input"
          placeholder="Enter your first name"
          type="text"
          value={firstName}
          onChange={handleFirstNameChange} />
      </FormGroup>

      <FormGroup
        label="Last Name"
        labelFor="last-name-input">      
        <InputGroup
          id="last-name-input"
          placeholder="Enter your last name"
          type="text"
          value={lastName}
          onChange={handleLastNameChange} />
      </FormGroup>

      <Button
        id="submit-btn"
        large={true}
        minimal={true}
        outlined={true}
        type="submit" 
        onClick={handleSubmit}>
          Register
      </Button>
    </div>
  );
};

export default RegisterForm