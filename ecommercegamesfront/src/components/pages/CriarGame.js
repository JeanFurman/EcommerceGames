import { useNavigate } from 'react-router-dom'
import GameForm from '../game/GameForm'
import styles from './CriarGame.module.css'

export default function CriarGame(){

    const navigate = useNavigate()

    function criarGame(formData){
        fetch('http://localhost:8001/games', {
            method: 'POST',
            body: formData
        })
        .then((resp) => resp.json())
        .then(() => {
            navigate('/')
        })
        .catch((err) => console.log())
    }

    return (
        <div className={styles.form}>
            <h1>Criar game</h1>
            <p>Adicione um game ao sistema</p>
            <GameForm handleSubmit={criarGame} btnText='Criar'/>
        </div>
    )
}