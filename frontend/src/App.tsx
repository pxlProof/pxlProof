import { Route } from "react-router-dom";
import { Routes } from "react-router-dom";
import "./App.css";
import Home from "./pages/Home/Home";
import Test from "./pages/Test/Test";
import Header from "./components/header/Header";

function App() {
  return (
    <>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/test" element={<Test />} />
      </Routes>
    </>
  );
}

export default App;
