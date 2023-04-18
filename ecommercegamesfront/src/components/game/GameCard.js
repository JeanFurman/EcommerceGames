import styles from './GameCard.module.css'
import { BsPencil, BsFillTrashFill} from 'react-icons/bs'
import { Link, useNavigate } from 'react-router-dom'

export default function GameCard({id, name, genero, plataforma, valor, imagem, quantidade, handleRemove, editGame}){

    const navigate = useNavigate()

    const remove = (e) =>{
        e.preventDefault()
        handleRemove(id)
    }

    function atualizar(){
        let json = JSON.stringify(editGame)
        localStorage.setItem('game', [json])
    }

    function details(){
        navigate(`/details/${id}`)
    }

    return(
        <div className={styles.gameCard}>
            <img src={`http://localhost:8001/games/imagens/${imagem}`} />
            <div>
                <h4 onClick={details}>{name}</h4>    
                <p>
                    Gênero: {genero}
                </p>
                <p>
                    Plataforma: {plataforma}
                </p>
                <p className={quantidade === 0 ? styles.indisponivel : styles.disponivel}>
                    {quantidade === 0 ? 'Indisponível' : 'Disponível'}
                </p>
                <span>R${valor}</span>
                <div className={styles.card_actions}>
                    <Link onClick={() => atualizar()} to={`/attgame/${id}`}><BsPencil/>Editar</Link>
                    <button onClick={remove}>
                        <BsFillTrashFill/>Excluir
                    </button>
                </div>
            </div>
        </div>
    )
}