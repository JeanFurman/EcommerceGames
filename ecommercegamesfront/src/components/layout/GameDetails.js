import styles from './GameDetails.module.css'

export default function GameDetails({text, value}){

    return(
        <div className={styles.details}>
            <label>{text}</label>
            <p>{value}</p>
        </div>         
    )
}