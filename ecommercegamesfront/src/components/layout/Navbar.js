import styles from './Navbar.module.css'
import { Link, useNavigate } from "react-router-dom";
import Container from "./Container";
import controle from '../../img/controle.png'


export default function Navbar(){

    const navigate = useNavigate()

    function limparToken(){
        localStorage.removeItem('token')
        navigate('/')
    }

    return (
        <nav className={styles.navbar}>
            <Container>
                <Link to='/'>
                    <img src={controle} alt='Games'/>
                </Link>
                <ul>
                    <li><Link to='/carrinho'>Carrinho</Link></li>
                    {localStorage.getItem('token') != null? 
                    <li><Link onClick={() => limparToken()}>Logout</Link></li> : 
                    <li><Link to='/login'>Login/Cadastro</Link></li>}
                    
                </ul>
            </Container>
        </nav>
    )
}