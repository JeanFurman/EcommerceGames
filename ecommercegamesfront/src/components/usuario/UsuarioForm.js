import styles from './UsuarioForm.module.css'
import Input from '../form/Input'
import Select from '../form/Select'
import BtnSubmit from '../form/BtnSubmit'
import { useState } from 'react'

export default function UsuarioForm({ handleSubmit, btnText, usuarioData }){

    // const privilegios = ['ADMIN', 'USER']
    const [usuario, setUsuario] = useState(usuarioData || {})

    const submit = (e) => {
        e.preventDefault()
        handleSubmit(usuario)
    }

    const handleChange = (e) => {
        setUsuario({...usuario, [e.target.name]: e.target.value})
    }

    return(
        <form onSubmit={submit} className={styles.form}>
            <Input type='text' text='Nome' name='nome' placeholder='Digite seu nome' handleOnChange={handleChange} value={usuario.nome ? usuario.nome : ''}/>
            <Input type='email' text='Email' name='email' placeholder='Digite um email válido' handleOnChange={handleChange} value={usuario.email ? usuario.email : ''}/>
            <Input type='password' text='Senha' name='senha' placeholder='Digite sua senha' handleOnChange={handleChange} />
            {/* <Select name='privilegio' text='Selecione um privilégio' options={privilegios} handleOnChange={handleChange}/> */}
            <BtnSubmit text={btnText}/>
        </form>
    )
}