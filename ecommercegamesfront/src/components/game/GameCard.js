import styles from './GameCard.module.css'
import { BsPencil, BsFillTrashFill} from 'react-icons/bs'
import { Link } from 'react-router-dom'

export default function GameCard({id, name, genero, plataforma, valor, handleRemove, editGame}){

    const remove = (e) =>{
        e.preventDefault()
        handleRemove(id)
    }

    function atualizar(){
        let json = JSON.stringify(editGame)
        localStorage.setItem('game', json)
    }

    return(
        <div className={styles.gameCard}>
            <h4>{name}</h4>
            <p>
                Gênero: {genero}
            </p>
            <p>
                Plataforma: {plataforma}
            </p>
            <span>R${valor}</span>
            <div className={styles.card_actions}>
                <Link onClick={() => atualizar()} to={`/attgame/${id}`}><BsPencil/>Editar</Link>
                <button onClick={remove}>
                    <BsFillTrashFill/>Excluir
                </button>
            </div>
        </div>
    )
}