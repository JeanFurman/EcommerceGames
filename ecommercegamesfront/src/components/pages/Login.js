import styles from './Usuario.module.css'
import LoginForm from '../usuario/LoginForm'

export default function Login(){

    function fazerLogin(usuario){
        fetch('http://localhost:8001/usuario/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(usuario)
        })
        .then((resp) => resp.json())
        .then((data) => {
            localStorage.setItem('token', data['access_token'])
            window.location.href = "http://localhost:3000/"
        })
        .catch((err) => console.log(err))
    }

    return (
        <div className={styles.form}>
            <h1>Login</h1>
            <LoginForm handleSubmit={fazerLogin} btnText='Entrar'/>          
        </div>
    )
}