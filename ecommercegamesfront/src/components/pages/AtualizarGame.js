import { useNavigate, useParams } from 'react-router-dom'
import GameForm from '../game/GameForm'
import styles from './CriarGame.module.css'

export default function Game(){

    const navigate = useNavigate()
    const { id } = useParams()
    const game = JSON.parse(localStorage.getItem('game'))

    function updateGame(game){
        fetch(`http://localhost:8001/games/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(game)
        })
        .then((resp) => resp.json())
        .then(() => {
            localStorage.removeItem('game')
            navigate('/')
        })
        .catch((err) => console.log())
    }

    return (
        <div className={styles.form}>
            <h1>Atualizar game</h1>
            <GameForm handleSubmit={updateGame} btnText='Atualizar' gameData={game}/>
        </div>
    )
}