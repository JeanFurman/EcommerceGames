import styles from './Navbar.module.css'
import { Link } from "react-router-dom";
import Container from "./Container";
import controle from '../../img/controle.png'
import { useState, useLayoutEffect } from 'react';
import { FaShoppingCart } from 'react-icons/fa'


export default function Navbar(){

    const [open, setOpen] = useState(false)
    const [nome, setNome] = useState()
    const [error, setError] = useState(false)
   
    useLayoutEffect(() => {
        console.log('entrei')
        if (localStorage.getItem('token') != null) {
            fetch('http://localhost:8001/usuario/me', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem("token")}`
            }
            })
            .then(async response => {
                const data = await response.json()
                localStorage.setItem('nome', data.nome)
                setNome(data.nome)
            }, async () => {
                setError(true)
            }) 
        }
    }, [nome])
    
    function limparToken(){
        localStorage.removeItem('token')
        localStorage.removeItem('nome')
        window.location.href = 'http://localhost:3000/'
    }

    function Dropdown(){
        return (
            <div>
                <div className={styles.menu_trigger} onClick={() => {setOpen(!open)}}>
                    <p>{nome && nome}</p>
                </div>
                {open && <div className={styles.dropdown_menu}>
                            <ul>
                                <li className={styles.dropdown_item}><Link onClick={() => {window.location.href = 'http://localhost:3000/perfil'}}>Perfil</Link></li>
                                <li className={styles.dropdown_item}><Link onClick={() => {window.location.href = 'http://localhost:3000/historico'}}>Histórico</Link></li>
                                <li className={styles.dropdown_item}><Link onClick={() => limparToken()}>Logout</Link></li> 
                            </ul>
                        </div>
                }
            </div>
        )
    }

    return (
        <nav className={styles.navbar}>
            <Container>
                <Link to='/'>
                    <img src={controle} alt='Games'/>
                </Link>
                <ul className={styles.ulnavbar}>
                    <li className={styles.linavbar}>
                        <Link to='/carrinho'>Carrinho <FaShoppingCart/></Link>
                    </li>
                    {localStorage.getItem('token') != null? 
                    <li><Dropdown/></li>: 
                    <li className={styles.linavbar}>
                        <Link to='/login'>Login/Cadastro</Link>
                    </li>}
                    
                </ul>
                {console.log(localStorage.getItem('token'))}
            </Container>
        </nav>
    )
}