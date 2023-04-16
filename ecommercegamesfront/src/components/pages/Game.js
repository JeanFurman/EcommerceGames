import { useNavigate, useParams } from "react-router-dom"
import { useState, useEffect } from "react"
import styles from './Game.module.css'
import GameDetails from "../layout/GameDetails"

export default function Game(){

    const { id } = useParams()
    const [game, setGame] = useState([])
    const navigate = useNavigate()

    useEffect(() => {
        fetch(`http://localhost:8001/games/${id}`)
        .then((resp) => resp.json())
        .then((data) => {
            setGame(data)
        })
        .catch((err) => console.log(err))
    }, [])

    const carrinho = () => {
        navigate('/')
    }

    return(
        <div className={styles.game_details}>
            <div className={styles.div_nome}>
                
                <h1>{game.nome}</h1>
                <GameDetails text={'Descrição'} value={game.descricao}/>
                <GameDetails text={'Desenvolvedor'} value={game.desenvolvedor}/>
                <GameDetails text={'Plataforma'} value={game.plataforma}/>
                <GameDetails text={'Gênero'} value={game.genero}/>
                <GameDetails text={'Preço'} value={`R$ ${game.valor}`}/>
                <button onClick={carrinho}>Comprar</button>
            </div>
            <div className={styles.div_image}>
                <img className={styles.game_image} src={`http://localhost:8001/games/imagens/${game.imagem}`} />
            </div>
        </div>
            
        
    )
}