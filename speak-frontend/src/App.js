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
    //const toBase64 = require('arraybuffer-base64');
    //const fd = new FormData();
    //console.log(recordedBlob);

    var fileReader = new FileReader();
    fileReader.onload = function(event) {
      const uuidv1 = require('uuid/v1');
      const toBase64 = require('arraybuffer-base64');
      var res = event.originalTarget.result;
      res = toBase64(res);
      axios.post('http://35.0.134.97:5000/submit_audio', {
        uuid:uuidv1(),
        file:res
      })
      .then(function (response) {
        this.setState({
          uuid: response.data.data.uuid
        });
      }.bind(this))
      .catch(function(error) {
        console.log(error)
      });
    }.bind(this);
    fileReader.readAsArrayBuffer(recordedBlob.blob);


    //var base64Version = toBase64(arrayBuffer);
    //fd.append("file",recordedBlob.blob,"file.webm")
  }

  componentWillMount() {
    axios.get('http://35.0.134.97:5000/').then(function(response) {
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
          onStop={this.onStop}
           />
        <button onClick={this.startRecording} type="button">Start</button>
        <button onClick={this.stopRecording} type="button">Stop</button>
      </div>
    );
  }
}

export default App;
