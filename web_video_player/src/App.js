import React, { Component } from 'react';
import './App.css';
import Budget from './Budget.js';
import ReactPlayer from "react-player";


class App extends Component { 
  render() {
    return (
      <div className="App">
        <Budget />
        
        <ReactPlayer url="https://5grealtimecommunication.s3-us-west-1.amazonaws.com/ferris_wheel_1280X720.mp4" control={true} />

        <h1> </h1>
        <ReactPlayer url="https://www.youtube.com/watch?v=yylt8-xTOVw&t=11s" control={true} />

        
        <button>Press</button>

      </div>
    );
  }
}



export default App;


