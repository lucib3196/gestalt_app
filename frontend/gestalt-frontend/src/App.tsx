import ListGroup from "./components/ListGroup";
import Alert from "./components/Alert";
import { Button } from "./components/Button";
import { useState } from "react";
import ModuleList from "./components/ModuleList";
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

function App(){
  return <div>App
    <ModuleList />
  </div>
}
export default App;
