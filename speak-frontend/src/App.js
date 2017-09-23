import React, { Component } from 'react';
import axios from 'axios';
import './App.css';
import { ReactMic } from 'react-mic';
import uuid from 'uuid';

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      id: null,
      record: false,
      uuid:null
    }

    this.onStop = this.onStop.bind(this);
  }

  startRecording = () => {
    this.setState({
      record: true
    });
  }

  stopRecording = () => {
    this.setState({
      record: false
    });
  }

  onStop(recordedBlob) {
    const uuidv1 = require('uuid/v1');
    console.log(recordedBlob);
    axios.post('http://35.3.108.250:5000/submit_audio', {
      uuid:uuidv1(),
      file:recordedBlob
    })
    .then(function (response) {
      this.setState({
        uuid: response.data.data.uuid
      });
    }.bind(this))
    .catch(function(error) {
      console.log(error)
    });
  }

  componentWillMount() {
    axios.get('http://35.3.108.250:5000/').then(function(response) {
      if (response.data.test && response.data.test.id) {
        this.setState({
          id: response.data.test.id
        });
      }
    }.bind(this));
  }

  render() {
    return (
      <div className="App">
        <ReactMic
          record={this.state.record}
          className="sound-wave"
          onStop={this.onStop}
          strokeColor="#000000"
          backgroundColor="#FF4081" />
        <button onClick={this.startRecording} type="button">Start</button>
        <button onClick={this.stopRecording} type="button">Stop</button>
        <p>{this.state.uuid}</p>
      </div>
    );
  }
}

export default App;
