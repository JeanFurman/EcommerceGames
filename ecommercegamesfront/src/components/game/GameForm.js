import styles from './GameForm.module.css'
import Input from '../form/Input'
import Select from '../form/Select'
import BtnSubmit from '../form/BtnSubmit'
import { useEffect, useState } from 'react'
import TextArea from '../form/TextArea'

export default function GameForm({ handleSubmit, btnText, gameData }){

    const [game, setGame] = useState(gameData || {})
    const [imageSelect, setImage] = useState()
    const [arquivo, setArquivo] = useState()
    const generos = ['FPS', 'BATTLE ROYALE', 'PVP', 'MOBA', 'RPG', 'MMORPG', 'AVENTURA', 'CORRIDA', 'RITMO']

    const submit = (e) => {
        e.preventDefault()
        const formData = new FormData();
        formData.append('nome', game.nome)
        formData.append('descricao', game.descricao)
        formData.append('genero', game.genero)
        formData.append('desenvolvedor', game.desenvolvedor)
        formData.append('plataforma', game.plataforma)
        formData.append('valor', game.valor)
        formData.append('file', imageSelect)
        handleSubmit(formData)
    }

    useEffect(() =>{
        console.log(game.nome)
    }, [game])

    const handleChange = (e) => {
        setGame({...game, [e.target.name]: e.target.value})
    }

    const handleValor = (e) => {
        setGame({...game, [e.target.name]: parseFloat(e.target.value)})
    }

    const handleImagem = (e) => {
        setImage(e.target.files[0])
        setArquivo(e.target.files[0].name)
    }


    return(
        <form onSubmit={submit} className={styles.form}>
            <div>
                <label className={styles.labelFile} htmlFor='image'>Enviar imagem</label>
                <input type='file' name='image' id='image' required accept='.jpeg, .jpg, .png' onChange={handleImagem}/> 
                <span>{arquivo}</span>
            </div>            
            <br/> 
            <Input type='text' text='Nome' name='nome' placeholder='Digite o nome' handleOnChange={handleChange} value={game.nome ? game.nome : ''}/>
            <TextArea rows='4' cols='10'name='descricao' text='Descrição' type='text' placeholder='Digite a descrição' handleOnChange={handleChange} value={game.descricao ? game.descricao : ''}/>
            {/* <Input type='text' text='Descrição' name='descricao' placeholder='Digite a descrição' handleOnChange={handleChange} value={game.descricao ? game.descricao : ''}/> */}
            <Input type='text' text='Desenvolvedor' name='desenvolvedor' placeholder='Digite o desenvolvedor' handleOnChange={handleChange} value={game.desenvolvedor ? game.desenvolvedor : ''}/>
            <Input type='text' text='Plataforma' name='plataforma' placeholder='Digite a plataforma' handleOnChange={handleChange} value={game.plataforma ? game.plataforma : ''}/>
            <Input type='number' text='Preço' name='valor' placeholder='Digite o preço' handleOnChange={handleValor} value={game.valor && game.valor}/>
            <Select name='genero' text='Selecione um gênero' options={generos} handleOnChange={handleChange} value={game.genero? game.genero : ''}/>             
            <BtnSubmit text={btnText}/>
        </form>
    )
}