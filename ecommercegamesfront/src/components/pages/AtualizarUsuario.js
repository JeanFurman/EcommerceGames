import UsuarioForm from '../usuario/UsuarioForm'
import styles from './Usuario.module.css'
import { useEffect, useLayoutEffect, useState } from 'react'


export default function Usuario(){

    const [usr, setUsr] = useState({})

    useLayoutEffect(() => {
        if(localStorage.getItem('token') != null){
            fetch('http://localhost:8001/usuario', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            })
            .then(async resp => {
                const data = await resp.json()
                localStorage.setItem('usuarioAtt', JSON.stringify(data))
                setUsr(data)
                console.log('user')})
            .catch((err) => console.log(err))
        }
    }, [])

    function atualizarUsuario(usuario){
        fetch(`http://localhost:8001/usuario/${usuario.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(usuario)
        })
        .then(async resp => {await resp.json()
            localStorage.removeItem('usuarioAtt')
            window.location.href = "http://localhost:3000/"
            })
        .catch((err) => console.log(err))
        console.log('ola')
    }

    return (
        <>
        {localStorage.getItem('token') &&
            <div className={styles.form}>
                <h1>Atualizar userPerfil</h1>
                <UsuarioForm handleSubmit={atualizarUsuario} btnText='Atualizar' usr={usr}/>
            </div>
        }
        </>
    )
}