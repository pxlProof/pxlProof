import { Route } from "react-router-dom";
import { Routes } from "react-router-dom";
import "./App.css";
import Home from "./pages/Home/Home";
import Test from "./pages/Test/Test";

function App() {
  return (
    <>
      <div>
        <h1>Hello World</h1>
      </div>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/test" element={<Test />} />
      </Routes>
    </>
  );
}

export default App;
