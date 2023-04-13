import { useNavigate } from 'react-router-dom'
import UsuarioForm from '../usuario/UsuarioForm'
import styles from './Usuario.module.css'

export default function Usuario(){

    const navigate = useNavigate()

    function criarUsuario(usuario){
        fetch('http://localhost:8001/usuario', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(usuario)
        })
        .then((resp) => resp.json())
        .then(() => {
            navigate('/')
        })
        .catch((err) => console.log(err))
    }

    return (
        <div className={styles.form}>
            <h1>Cadastro</h1>
            <p>Se registre agora para liberar as funcionalidades do sistema</p>
            <UsuarioForm handleSubmit={criarUsuario} btnText='Registrar-se'/>
        </div>
    )
}