import styles from './UsuarioForm.module.css'
import { useState } from 'react'
import { Link } from 'react-router-dom'
import BtnSubmit from '../form/BtnSubmit'
import Input from '../form/Input'

export default function LoginForm({ handleSubmit, btnText }){
    
    const [usuario, setUsuario] = useState({})
    
    const submit = (e) => {
        e.preventDefault()
        handleSubmit(usuario)
    }

    const handleChange = (e) => {
        setUsuario({...usuario, [e.target.name]: e.target.value})
    }

    return(
        <form onSubmit={submit} className={styles.form}>
            <Input type='email' text='Email' name='email' placeholder='Digite um email válido' handleOnChange={handleChange}/>
            <Input type='password' text='Senha' name='senha' placeholder='Digite sua senha' handleOnChange={handleChange} />
            {/* <Select name='privilegio' text='Selecione um privilégio' options={privilegios} handleOnChange={handleChange}/> */}
            <div>
                <BtnSubmit text={btnText}/>
                <Link className={styles.link_login} to='/usuario'>Cadastre-se</Link>
            </div>
        </form>
    )
}