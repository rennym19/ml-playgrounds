import React, { Component } from "react"
import { render } from "react-dom"
import Welcome from "./playgrounds/Welcome/Welcome"

import './App.css'

class App extends Component {
  render() {
    return <Welcome />
  }
}

export default App

const container = document.getElementById("app")
render(<App />, container)
