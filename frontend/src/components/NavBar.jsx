import React from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from 'react-router-dom';
import './NavBar.css';

import Home from './Home';
import ModuleTable from './Modules';

const NavbarStyle = () => {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <div className="container-fluid">
        <Link className="navbar-brand" to="/">
          Gestalt App
        </Link>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ms-auto">
            <li className="nav-item">
              <Link className="nav-link" to="/">
                Home
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/modules">
                Modules
              </Link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

const NavBar = () => {
  return (
    <Router>
      <NavbarStyle />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/modules" element={<ModuleTable />} />
      </Routes>
    </Router>
  );
};

export default NavBar;
