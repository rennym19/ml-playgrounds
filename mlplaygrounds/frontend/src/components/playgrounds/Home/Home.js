import React, { Component } from 'react'

import Cookie from 'js-cookie'

class Home extends Component {
  constructor(props) {
    super(props)

    this.state = {
      username: '',
      email: '',
      firstName: '',
      lastName: '',
      registrationDate: ''
    }

    this.logout = this.logout.bind(this)
  }

  componentDidMount() {
    fetch('users/profile/', {
      headers: {
        'Authorization': `Token ${this.props.token}`
      }
    })
    .then(res => res.json().then(data => ({status: res.status, body: data})))
    .then(
      result => {
        if (result.status === 200) {
          this.setState({
            username: result.body.username,
            email: result.body.email,
            firstName: result.body.first_name,
            lastName: result.body.last_name,
            registrationDate: result.body.registration_date
          })
        } else if (result.status === 401) {
          this.props.logoutHandler()
        } else {
          this.setState({
            error: result.body.error
          })
        } 
      }
    )
  }

  logout() {
    fetch('users/logout/', {
      method: 'POST',
      headers: {
        'Authorization': `Token ${this.props.token}`
      }
    })
    .then(res => {
      if (res.status == 204) {
        this.props.logoutHandler()
      } else {
        console.log('Error while logging out... Were you logged in?')
      }
    })
  }

  render() {
    return (
      <div>
        <h1>Welcome, {this.state.username}</h1>
        <a href="#" onClick={this.logout}>Logout</a>
      </div>
    )
  }
}

export default Home
