import { useNavigate, useParams } from "react-router-dom"
import { useState, useEffect } from "react"
import styles from './Game.module.css'
import GameDetails from "../layout/GameDetails"

export default function Game(){

    const { id } = useParams()
    const [game, setGame] = useState({})
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
        let gameData = []
        if(localStorage.hasOwnProperty('carrinho')){
            gameData.push(...JSON.parse(localStorage.getItem('carrinho')))
            gameData = gameData.filter((data) => data.id !== game.id)
        }
        console.log(game)
        gameData.push(game)
        localStorage.setItem('carrinho', JSON.stringify(gameData))
        navigate('/carrinho')
    }

    return(
        <div className={styles.game_details}>
            <div className={styles.div_nome}>
                
                <h1>{game.nome}</h1>
                <GameDetails text={'Descrição'} value={game.descricao}/>
                <GameDetails text={'Desenvolvedor'} value={game.desenvolvedor}/>
                <GameDetails text={'Plataforma'} value={game.plataforma}/>
                <GameDetails text={'Gênero'} value={game.genero}/>
                <div style={{display: 'flex', justifyContent: 'space-between'}}>
                <GameDetails text={'Preço'} value={`R$ ${game.valor}`}/>
                <GameDetails text={'Quantidade'} value={game.quantidade}/>
                </div>
                
                <button onClick={carrinho}>Comprar</button>
            </div>
            <div className={styles.div_image}>
                <img className={styles.game_image} src={game.imagem &&`http://localhost:8001/games/imagens/${game.imagem}`} />
            </div>
        </div>
            
        
    )
}