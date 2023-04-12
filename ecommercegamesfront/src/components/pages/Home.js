import styles from './Home.module.css' 
import { useState, useEffect } from 'react'

import BtnLink from '../layout/BtnLink'
import Container from '../layout/Container'

import GameCard from '../game/GameCard'

export default function Home(){

    const [games, setGames] = useState([])

    useEffect(() => {
        fetch('http://localhost:8001/games')
        .then((resp) => resp.json())
        .then((data) => {
            setGames(data)
        })
        .catch((err) => console.log(err))
    }, [])

    return (
        <div className={styles.home_container}>
            <div className={styles.btn_container}>
                <h1>Games Shop</h1>
                <BtnLink to='/criargame' text='Criar Game'/>
            </div>
            <Container customClass='start'>
                {games.length > 0 && 
                    games.map((game) => (
                        <GameCard id={game.id} name={game.nome} genero={game.genero} plataforma={game.plataforma} valor={game.valor} key={game.id}/>
                    ))}
            </Container>
        </div>
    )
}