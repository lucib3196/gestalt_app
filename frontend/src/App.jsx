// App.js
import React from 'react';
import './App.css';
import {
  BrowserRouter as Router,
  Routes,
  Route
} from "react-router-dom";

import ModuleTable from './components/Modules';
import Navbar from './components/NavBar';
import Home from './components/Home';
import ChatBot from './components/ChatBot';
// const App = () => {
//   return (
//     <Router>
//       <Navbar />
//       <Routes>
//         <Route path="/" element={<Home />} />
//         <Route path="/modules" element={<ModuleTable />} />
//       </Routes>
//     </Router>
//   );
// };

const App = ()=>{
  return (
    <ChatBot/>
  )
}

export default App;
