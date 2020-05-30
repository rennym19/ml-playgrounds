import React, { Component } from 'react'
import { Card, Button, Text } from '@blueprintjs/core'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faFrown } from '@fortawesome/free-solid-svg-icons'

import Nav from '../Nav/Nav'
import DatasetForm from '../Datasets/Forms/DatasetForm'
import './Home.css'

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
      <div id="Home">
        <Nav id="Navbar" username={this.state.username} logout={this.logout} />
        <div id="Content" className="no-datasets">
          <Card id="no-datasets">
            <FontAwesomeIcon className="card-icon" icon={faFrown} size="6x" />
            <Text className="card-msg">Looks like you don't have any datasets yet</Text>
            <Button className="card-btn" fill={true} minimal={true} text="Add Dataset" />
          </Card>
          <Card id="add-dataset-card">
            <DatasetForm />
          </Card>
        </div>
      </div>
    )
  }
}

export default Home
