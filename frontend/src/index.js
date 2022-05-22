import React from 'react';
import ReactDOM from 'react-dom';
import CanvasDraw from 'react-canvas-draw';
import reportWebVitals from './reportWebVitals';

function onMessage() {
  window.saveableCanvas.loadSaveData();
}

function onChange() {
  console.log(window.saveableCanvas.getSaveData());
}

ReactDOM.render(
  <CanvasDraw 
    ref={canvasDraw => (window.saveableCanvas = canvasDraw)}
    onChange={onChange}
    canvasWidth={window.innerWidth}
    canvasHeight={window.innerHeight}
    hideGrid={true}
    brushRadius={1}
    lazyRadius={0}
  />,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
