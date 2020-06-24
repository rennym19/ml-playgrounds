import React from 'react'
import data_image from './images/undraw_data_xmfy.svg'

import './AppInfo.css'

const AppInfo = (props) => {
  return (
    <div className="AppInfo">
      <h1>ML Playgrounds</h1>
      <h4>
        Upload your datasets and play around with them using multiple 
        Machine Learning, Data Science and Statistics tools.
      </h4>
      <img src={data_image} alt="Data manipulation by ML Playgrounds"/>
    </div>
  )
};

export default AppInfo