// App.js
import React from 'react';
import './App.css';
import {
  BrowserRouter as Router,
  Routes,
  Route
} from "react-router-dom";

import NavBar from './components/NavBar';



const App = () => {
  return (
    <NavBar/>
  );
};

// const App = ()=>{
//   return (
//     <ChatBot/>
//   )
// }

export default App;
