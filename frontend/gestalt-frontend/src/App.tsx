import ListGroup from "./components/ListGroup";
import Alert from "./components/Alert";
import { Button } from "./components/Button";
import { useState } from "react";
import ModuleList from "./components/ModuleList";

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import Navbar from "./components/Navbar";
import { Home } from "./components/Home";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import ModulePage from "./components/ModulePage";
import GeneratorPage from "./components/GeneratorPage";
import "./App.css"


// function App() {
//   const [alertVisible, setAlertVisibility] = useState(false);

//   let items = ["New York", "San Francisco", "Tokyo"];
//   const handleSelectItem = (item: string) => {
//     console.log(item);
//   };
//   return (
//     <div>
//       <ListGroup
//         items={items}
//         heading={"Cities"}
//         onSelectItem={handleSelectItem}
//       />
//       {alertVisible && (
//         <Alert onClick={() => setAlertVisibility(false)}>
//           <h1>This is an alert</h1> <p>This is a paragraph</p>
//         </Alert>
//       )}

//       <Button color="primary" onClick={() => setAlertVisibility(true)}>
//         I am a button
//       </Button>
//     </div>
//   );
// }

// function App(){
//   return <div>App
//     <ModuleList />
//   </div>
// }

const app_name = "Gestalt App";

const links = [
  { name: "Home", ref_link: "/" },
  { name: "About", ref_link: "#about" },
  { name: "Modules", ref_link: "/modules" },
  { name: "Generators", ref_link: "/generators" },
];

const routeComponents = {
  Home: <Home />,
  Modules: <ModulePage />,
  Generators: <GeneratorPage />,
};

type RouteName = keyof typeof routeComponents;

function handleLinks() {
  return links
    .filter((link): link is { name: RouteName; ref_link: string } =>
      Object.keys(routeComponents).includes(link.name)
    )
    .map((link, idx) => (
      <Route
        path={link.ref_link}
        key={idx}
        element={routeComponents[link.name]}
      />
    ));
}

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar app_name={app_name} links={links} />
        <div className="content">
          <Routes>{handleLinks()}</Routes>
        </div>
      </div>
    </Router>
  );
}
export default App;
