import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Container from "./components/layout/Container";
import Navbar from "./components/layout/Navbar";

import Home from "./components/pages/Home";
import CriarGame from "./components/pages/CriarGame";
import Game from "./components/pages/Game";
import Footer from "./components/layout/Footer";

function App() {
  return (
    <Router>
      <Navbar/>
      <Container customClass='min-height'>
        <Routes>
          <Route exact path="/" element={<Home/>}/>
          <Route path="/criargame" element={<CriarGame/>}/>
          <Route path="/game" element={<Game/>}/>
        </Routes>
      </Container>
      <Footer/>
    </Router>
  );}

export default App;
