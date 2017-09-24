import React, { Component } from 'react';
import axios from 'axios';
import './App.css';
import { ReactMic } from 'react-mic';
import uuid from 'uuid';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip,
   Legend, Radar, RadarChart, PolarGrid, PolarRadiusAxis, PolarAngleAxis,
 BarChart, Bar, ReferenceLine, AreaChart, Area} from 'recharts';

 import { Button, Row, Col, Panel } from 'react-bootstrap';

 function CreateLineChart(props){
   return(
     <LineChart width={600} height={300} data={props.LineData}
         margin={{top: 5, right: 30, left: 20, bottom: 5}}>
         <XAxis dataKey="name"/>
         <YAxis/>
         <CartesianGrid strokeDasharray="3 3"/>
         <Tooltip/>
         <Legend />
         <Line type="monotone" dataKey="stutterwordpercent" stroke="#8884d8" activeDot={{r: 8}}/>
         <Line type="monotone" dataKey="duplicatepercent" stroke="#82ca9d" />
    </LineChart>
   )
 }
 function CreateRadarChart(props) {
   return(
     <RadarChart cx={300} cy={250} outerRadius={150} width={600} height={500} data={props.RadarData}>
       <Radar name="Sentiments" dataKey="A" stroke="#8884d8" fill="#8884d8" fillOpacity={0.9}/>
       <PolarGrid />
       <PolarAngleAxis dataKey="subject" />
       <PolarRadiusAxis />
     </RadarChart>
   )
 }
 function CreateAreaChart(props){
   return(
     <AreaChart width={600} height={200} data={props.AreaData}
           margin={{top: 10, right: 30, left: 0, bottom: 0}}>
       <XAxis dataKey="name"/>
       <YAxis/>
       <CartesianGrid strokeDasharray="3 3"/>
       <Tooltip/>
       <Area connectNulls={true} type='monotone' dataKey='wpm' stroke='#8884d8' fill='#8884d8' />
     </AreaChart>
   )
 }
 function CreateVisualGraphics(props) {
   if(props.flagRender){
     return(
       <div>
         <Row>
           <Col xs={6}>
             <Panel>
               <p>{props.text}</p>
             </Panel>
           </Col>
           <Col xs={6}>
             <Panel>
               <h4>Stutter and Duplicate Percentages for your speech</h4>
               <CreateLineChart LineData={props.LineData}></CreateLineChart>
               <h4>Sentiment Analysis of your speech</h4>
               <CreateRadarChart RadarData={props.RadarData}></CreateRadarChart>
               <h4>Words Per Minute Trends</h4>
               <CreateAreaChart AreaData={props.AreaData}></CreateAreaChart>
             </Panel>
           </Col>
         </Row>
       </div>
     )
   } else {
     return(
       <div>
         <h1>Record To Show Statistics</h1>
       </div>
     )
   }
 }
 function CreateReactMic(props) {
   if(props.showMic){
     return(
       <h3>Reload page to try another file</h3>
     )
   } else {
     return(
       <div>
         <Row>
           <ReactMic
             record={props.record}
             onStop={props.onStop}
             strokeColor='#ff5733'
            />
        </Row>
        <Row>
          <Button bsStyle="default" bsSize="large" onClick={props.start}>
            Start
          </Button>
          <Button bsStyle="default" bsSize="large" onClick={props.stop}>
            Stop
          </Button>
        </Row>
      </div>
     )
   }
 }

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      id: null,
      record: false,
      uuid:null,
      disp_results:false,
      data:{
        'text': 'Hey Just teting to see if this works',
        'LineData': [
          {'duplicatepercent': 0, 'stutterwordpercent': 0}
        ],
        'RadarData': [
          { subject: 'Anger', A: 0, fullMark: .69 },
          { subject: 'Disgust', A: 0,fullMark: .69 },
          { subject: 'Sadness', A: 0,fullMark: .69 },
          { subject: 'Joy', A: 0, fullMark: .69 },
          { subject: 'Fear', A: 0,fullMark: .69 },
        ],
        'AreaData': [
            {'wpm': 0},
            {'wpm': 0},
            {'wpm': 0},
            {'wpm': 0},
            {'wpm': 0},
            {'wpm': 0},
            {'wpm': 0},
        ]
      }
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

  componentWillMount() {
    axios.get('http://35.3.108.250:5000/').then(function(response) {
      if (response.data.test && response.data.test.id) {
        this.setState({
          id: response.data.test.id
        });
      }
    }.bind(this));
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
      axios.post('http://35.3.108.250:5000/submit_audio', {
        uuid:uuidv1(),
        file:res
      })
      .then(function (response) {
        var analysis = response.data.data.analysis;
        //console.log(analysis);
        var line = [];
        for(var i=0; i < analysis['fillerWords'].length; i = i + 1) {
          line.push({ 'duplicatepercent': analysis['duplicate'][i] , 'stutterwordpercent':analysis['fillerWords'][i] });
        }

        var radar = [
          { subject: 'Anger', A: analysis['anger'], fullMark: .69 },
          { subject: 'Disgust', A: analysis['disgust'],fullMark: .69 },
          { subject: 'Sadness', A: analysis['sadness'],fullMark: .69 },
          { subject: 'Joy', A: analysis['joy'], fullMark: .69 },
          { subject: 'Fear', A: analysis['fear'],fullMark: .69 },
        ];

        var area = [];
        for(var i=0; i < analysis['avg_wpm'].length; i = i + 1) {
          area.push({ 'wpm': analysis['avg_wpm'][i] });
        }

        console.log(line);
        console.log(radar);
        console.log(area);
        this.setState({
          uuid: response.data.data.uuid,
          data: {
            'text':analysis.text,
            'LineData' : line,
            'RadarData' : radar,
            'AreaData' : area
          },
          disp_results: true,
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

  render() {
    return (
      <div className="App">
        <CreateReactMic start={this.startRecording} stop={this.stopRecording} record={this.state.record} onStop={this.onStop} showMic={this.state.disp_results}/>
        <CreateVisualGraphics text={this.state.data.text} LineData={this.state.data.LineData} RadarData={this.state.data.RadarData} AreaData={this.state.data.AreaData} flagRender={this.state.disp_results}></CreateVisualGraphics>
      </div>
    );
  }
}

export default App;
