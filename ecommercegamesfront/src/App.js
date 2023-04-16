import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Container from "./components/layout/Container";
import Navbar from "./components/layout/Navbar";
import Footer from "./components/layout/Footer";

import Home from "./components/pages/Home";
import CriarGame from "./components/pages/CriarGame";
import AtualizarGame from "./components/pages/AtualizarGame";
import Usuario from "./components/pages/Usuario";
import Login from "./components/pages/Login";
import AtualizarUsuario from './components/pages/AtualizarUsuario'
import Game from "./components/pages/Game";


function App() {
  return (
    <Router>
      <Navbar/>
      <Container customClass='min-height'>
        <Routes>
          <Route exact path="/" element={<Home/>}/>
          <Route path="/criargame" element={<CriarGame/>}/>
          <Route path="/attgame/:id" element={<AtualizarGame/>}/>
          <Route path="/usuario" element={<Usuario/>}/>
          <Route path="/login" element={<Login/>}/>
          <Route path="/details/:id" element={<Game/>}/>
          <Route path="/perfil" element={<AtualizarUsuario/>}/>
        </Routes>
      </Container>
      <Footer/>
    </Router>
  );}

export default App;
