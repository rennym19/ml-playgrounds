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
    fetch('users/profile/')
    .then(res => res.json())
    .then(
      (result) => {
        this.setState({
          username: result.username,
          email: result.email,
          firstName: result.first_name,
          lastName: result.last_name,
          registrationDate: result.registration_date
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

  logout() {
    fetch('users/logout/', {
      method: 'POST',
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