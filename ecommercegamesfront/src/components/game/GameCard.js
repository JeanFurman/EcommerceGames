import styles from './GameCard.module.css'

export default function GameCard({id, name, genero, plataforma, valor}){
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
        </div>
    )
}