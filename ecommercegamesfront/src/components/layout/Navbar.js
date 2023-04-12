import styles from './Navbar.module.css'
import { Link } from "react-router-dom";
import Container from "./Container";
import controle from '../../img/controle.png'


export default function Navbar(){
    return (
        <nav className={styles.navbar}>
            <Container>
                <Link to='/'>
                    <img src={controle} alt='Games'/>
                </Link>
                <ul>
                    <li><Link to='/carrinho'>Carrinho</Link></li>
                    <li><Link to='/sds'>Login</Link></li>
                </ul>
            </Container>
        </nav>
    )
}