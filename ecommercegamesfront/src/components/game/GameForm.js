import styles from './GameForm.module.css'
import Input from '../form/Input'
import Select from '../form/Select'
import BtnSubmit from '../form/BtnSubmit'
import { useEffect, useState } from 'react'

export default function GameForm({ handleSubmit, btnText, gameData }){

    const [game, setGame] = useState(gameData || {})
    const generos = ['FPS', 'BATTLE ROYALE', 'PVP', 'MOBA', 'RPG', 'MMORPG', 'AVENTURA', 'CORRIDA', 'RITMO']

    const submit = (e) => {
        e.preventDefault()
        handleSubmit(game)
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
        setGame({...game, [e.target.name]: e.target.files[0]})
    }


    return(
        <form onSubmit={submit} className={styles.form}>
            <Input type='text' text='Nome' name='nome' placeholder='Digite o nome' handleOnChange={handleChange} value={game.nome ? game.nome : ''}/>
            <Input type='text' text='Descrição' name='descricao' placeholder='Digite a descrição' handleOnChange={handleChange} value={game.descricao ? game.descricao : ''}/>
            <Input className={styles.desc} type='text' text='Desenvolvedor' name='desenvolvedor' placeholder='Digite o desenvolvedor' handleOnChange={handleChange} value={game.desenvolvedor ? game.desenvolvedor : ''}/>
            <Input type='text' text='Plataforma' name='plataforma' placeholder='Digite a plataforma' handleOnChange={handleChange} value={game.plataforma ? game.plataforma : ''}/>
            <Input type='number' text='Preço' name='valor' placeholder='Digite o preço' handleOnChange={handleValor} value={game.valor && game.valor}/>
            <input type='file' name='imagem' onChange={handleImagem}/>
            <Select name='genero' text='Selecione um gênero' options={generos} handleOnChange={handleChange} value={game.genero? game.genero : ''}/>
            <BtnSubmit text={btnText}/>
        </form>
    )
}