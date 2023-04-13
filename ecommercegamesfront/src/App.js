import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Container from "./components/layout/Container";
import Navbar from "./components/layout/Navbar";
import Footer from "./components/layout/Footer";

import Home from "./components/pages/Home";
import CriarGame from "./components/pages/CriarGame";
import Game from "./components/pages/Game";
import Usuario from "./components/pages/Usuario";
import Login from "./components/pages/Login";


function App() {
  return (
    <Router>
      <Navbar/>
      <Container customClass='min-height'>
        <Routes>
          <Route exact path="/" element={<Home/>}/>
          <Route path="/criargame" element={<CriarGame/>}/>
          <Route path="/game" element={<Game/>}/>
          <Route path="/usuario" element={<Usuario/>}/>
          <Route path="/login" element={<Login/>}/>
        </Routes>
      </Container>
      <Footer/>
    </Router>
  );}

export default App;
